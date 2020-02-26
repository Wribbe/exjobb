try:
  from utils import \
    get_db, dump_vars, as_percent, iter_markers, iter_colors, run_successful
  from utils import extractor
except ImportError:
  from msccls.figures.utils import \
    get_db, dump_vars, as_percent, iter_markers, iter_colors, run_successful
  from msccls.figures.utils import extractor

import os

import matplotlib.pyplot as plt
from datetime import datetime, timezone, timedelta


def get_data():

  db = get_db()
  testruns = db.execute("SELECT * FROM test_run WHERE t_stop").fetchall()
  testruns = fixtestruns(testruns)
  db.close()

#  for run in testruns:
#    print(run['t_start'], run['t_stop'])


def run_to_datetime(run):
  start = datetime.strptime(run['t_start'], '%Y-%m-%d %H:%M:%S.%f%Z')
  stop = datetime.strptime(run['t_stop'], '%Y-%m-%d %H:%M:%f%Z')
  return start, stop


def fixtestruns(testruns):

  found_total, left = nom_nom(testruns)
  for i in range(5):
    total, left = nom_nom(left)
    found_total += total

  for (user, run), sec in zip([(r['id_user'], r) for r in left], [2,10]):
    start, stop = run_to_datetime(run)
    temp = start + timedelta(seconds=sec)
    found_total.append((user, (run, start, stop.replace(second=temp.second))))

  ret = []
  for (_, (run, start, stop)) in found_total:
    run = dict(run)
    stop = stop.replace(tzinfo=timezone.utc)
    run['t_stop'] = datetime.strftime(stop, '%Y-%d-%m %H:%M:%S.%f%Z')
    ret.append(run)
  return ret

def nom_nom(testruns, silent=True):

  stamps = {}
  runs_by_user = {}
  found = []
  left = []

  def timestamp(date, remove_micro=True):
    try:
      date = date.replace(microsecond=0)
    except AttributeError:
      date, _ = run_to_datetime(date)
      return timestamp(date)
    return int(date.timestamp())

  def status():
    num_found = len(found)
    num_left = len(left)
    print(f"Percent found: {num_found/len(testruns)*100:.2f}%, {len(left)} of {len(left+found)} remaining.")

  def line_to_ip(line):
    return line.split(' ')[0]

  # Log data in correct UTC times at timestamps.
  log_data = {timestamp(k):v for k,v in extractor.get().items()}
  post_events_dic = {}
  pattern_posts = {}
  for stamp, lines in log_data.items():
    for line in lines:
      event_type = None
      if 'GET' in line:
        event_type = 'GET'
      elif 'POST' in line:
        event_type = 'POST'
      if event_type:
        pattern_posts.setdefault(stamp, []).append(event_type)
      if not event_type == 'POST':
        continue
      post_events_dic.setdefault(stamp, []).append(line)

  runs_per_user = {}
  for run in testruns:
    user = run['id_user']
    start, _ = run_to_datetime(run)
    stamp = timestamp(start)
    runs_per_user.setdefault(user, []).append(run)
    left.append((run['id_user'], run))

  users_at_timestamp = {}
  starts = {}
  info = {}
  slices_per_user = {}
  ips_per_user = {}

  for user, runs in runs_per_user.items():
    for run, run_next in zip(runs, runs[1:]+[None]):
      start, stop = run_to_datetime(run)
      start = timestamp(start, remove_micro=False)
      stop = timestamp(stop + timedelta(minutes=1))
      start_next = timestamp(datetime.utcnow())
      if run_next:
        start_next, _ = run_to_datetime(run_next)
        start_next = timestamp(start_next)
      stop = min([stop, start_next])
      slices_per_user.setdefault(user, []).append((start, stop, run))
      starts.setdefault(start, []).append((user, run))
      stamp = start
      while stamp < stop:
        users_at_timestamp.setdefault(stamp, set()).add(user)
        post_events = post_events_dic.get(stamp)
        if post_events:
          info.setdefault(stamp, [])
          info[stamp] += post_events
          for event in post_events:
            ips_per_user.setdefault(user, {})
            ip = line_to_ip(event)
            ips_per_user[user].setdefault(ip, 0)
            ips_per_user[user][ip] += 1
        stamp += 1

  def only_one_at_slice(tup):
    start, stop, _ = tup
    for i in range(start, stop):
      if len(users_at_timestamp[i]) > 1:
        return False
    return True

  def get_posts_for_slice(tup, exclude_start=True):
    start, stop, _ = tup
    posts = []
    for i in range(start, stop):
      posts += [(i, post) for post in post_events_dic.get(i, [])]
    if exclude_start:
      posts = [(s,p) for s,p in posts if s != start]
    return posts

  unique_ips = {}
  for user, slices in slices_per_user.items():
    if user in unique_ips:
      continue
    for tup in slices:
      if only_one_at_slice(tup):
        ip_set = set()
        for _, post in get_posts_for_slice(tup):
          ip_set.add(line_to_ip(post))
        if len(ip_set) == 1:
          if user in unique_ips:
            raise Exception("Found more than one unique ip?")
          unique_ips[user] = list(ip_set)[0]
          break

  def filter_posts_on_ip(posts, ip):
    ret = []
    for stamp, post in posts:
      if not ip == line_to_ip(post):
        continue
      ret.append((stamp, post))
    return ret

  start_ids = {}
  for stamp, users in starts.items():
    if len(users) > 1:
      continue
    user, run = users[0]
    posts = post_events_dic.get(stamp, [])
    if len(posts) == 1:
      start_ids.setdefault(user, set()).add(line_to_ip(posts[0]))

  for user, ips in start_ids.items():
    ip = list(ips)[0]
    if user not in unique_ips:
      unique_ips[user] = ip

  users_per_ip = {}
  for user, ip in unique_ips.items():
    users_per_ip.setdefault(ip, set()).add(user)
  users_per_ip = {k:list(v) for k,v in users_per_ip.items()}

  def remove_duplicate_posts(posts):
    seen_stamps = set()
    ret = []
    for stamp, post in posts:
      if stamp in seen_stamps:
        continue
      ret.append((stamp, post))
      seen_stamps.add(stamp)
    return ret

  found = []
  left = []

  users_at_line = {}
  for user, slices in slices_per_user.items():
    for tup in slices:

      posts = get_posts_for_slice(tup, exclude_start=True)
      ip = unique_ips.get(user)
      if ip:
        posts = filter_posts_on_ip(posts, ip)
      posts = remove_duplicate_posts(posts)
      for stamp, post in posts:
        users_at_line.setdefault(post, set()).add(user)

  for user, slices in slices_per_user.items():
    for tup in slices:
      alone = only_one_at_slice(tup)

      posts = get_posts_for_slice(tup, exclude_start=True)
      ip = unique_ips.get(user)
      if ip:
        posts = filter_posts_on_ip(posts, ip)
      posts = remove_duplicate_posts(posts)

      t_start, t_stop, run = tup

      start, stop = run_to_datetime(run)
      stamp_full = start.timestamp()

      if not silent:
        print(
          f"user: {user}, start: {stamp_full} ,slice: {(t_start, t_stop)}: " \
          f"alone: {alone} posts: {len(posts)} " \
          #f"single_ip: {len(users_per_ip[ip])}"
        )

      all_post_users = set()
      collisions = []
      non_collisions = []
      for stamp, post in posts:
        if len(users_at_line[post]) > 1:
          collisions.append(post)
        else:
          non_collisions.append((stamp, post))
        for user in users_at_line[post]:
          all_post_users.add(user)
      own_all_lines = len(all_post_users) == 1

      if alone or (not alone and own_all_lines):
#      if alone:
        submit = datetime.fromtimestamp(posts[0][0])
#        stop_old = stop
        stop = stop.replace(second=submit.second)
#        print(f'{str(stop_old)=}, {str(stop)=}, {str(start)=} diff:{stop-start}')
        found.append((user, (run, start, stop)))
      elif not alone and non_collisions:
        submit = datetime.fromtimestamp(non_collisions[0][0])
        stop = stop.replace(second=submit.second)
        found.append((user, (run, start, stop)))
      else:
        left.append(run)

      for stamp, post in posts:
        delta = datetime.fromtimestamp(stamp)-datetime.fromtimestamp(tup[0])
        pattern = pattern_posts[stamp]
        if not silent:
          print(f" {stamp} {post} {delta} {pattern} ")
      if not silent:
        print(f" Owns all lines: {own_all_lines} | {all_post_users}")
        print(f"  Colliding:")
        for line in collisions:
          print(f"    {line}")
        print(f"  Non Colliding:")
        for line in non_collisions:
          print(f"    {line}")
  status()
#  if not silent:
#    for stamp, users in users_at_timestamp.items():
#      print(f"{stamp}: {users}")
#  for line, users in users_at_line.items():
#    print(f"{line}: {users}")
  return found, left


if __name__ == "__main__":
  get_data()
