import os
from msccls.figures.utils import get_db, dump_vars, as_percent, incremental_sum

def get_data():
  db = get_db()
  testruns = db.execute("SELECT * FROM test_run").fetchall()
  users = db.execute("SELECT * FROM test_user").fetchall()
  db.close()
  runsPerUser = {}
  for run in testruns:
    idUser = run['id_user']
    runsPerUser.setdefault(idUser, 0)
    runsPerUser[idUser] += 1

  numberOfRuns = {}
  for user, val in sorted(runsPerUser.items(), key=lambda t: t[1]):
    numberOfRuns.setdefault(val, 0)
    numberOfRuns[val] += 1

  valNumAnyTestsRun = sum(numberOfRuns.values())
  valTestTenOrLess = 0
  valTestsElevenOrMore = 0
  vals = {}
  numUsersTotal = len(users)
  valTestNoTests = numUsersTotal - valNumAnyTestsRun
  numUsersDidTests = numUsersTotal-valTestNoTests
  for numRuns, numUsers in numberOfRuns.items():
    if numRuns < 11:
      valTestTenOrLess += numUsers
    elif numRuns > 10:
      valTestsElevenOrMore += numUsers
    vals.setdefault(numRuns, 0)
    vals[numRuns] += numUsers

#  for k,v in vals.items():
#    vals[k] = v/numUsersTotal

  valTestsElevenOrMoreP = as_percent(valTestsElevenOrMore/numUsersTotal)
  valTestTenOrLessP = as_percent(valTestTenOrLess/numUsersTotal)

  tx, ty = incremental_sum(numberOfRuns)
  tabular = [(
    "\\# Tests run",
    '\\# participants',
    "Sum participants",
    '\\% of total participating'
  )]
  tabular += [
    (fr"$\#r\leq{k}$", f"${numberOfRuns[k]}$", f"${v}$", f"${v/numUsersDidTests*100:.2f}\%$") for k,v in zip(tx, ty)
  ]
  tablePrecentageOfUsers = [rf"\begin{{tabular}}{{| l | c | c | c |}}"]
  tabular[1] = ('$\\#r=1$', *tabular[1][1:])
  for line in tabular:
    tablePrecentageOfUsers.append(f"\\hline {'&'.join(line)}\\\\")
  tablePrecentageOfUsers.append(rf"\hline\end{{tabular}}")
  tablePrecentageOfUsers = os.linesep.join(tablePrecentageOfUsers)

  dump_vars([
    ('valNumAnyTestsRun', valNumAnyTestsRun),
    ('valTestTenOrLess', valTestTenOrLess),
    ('valTestsElevenOrMore', valTestsElevenOrMore),
    ('valTestNoTests', valTestNoTests),
    ('valTestTenOrLessP', valTestTenOrLessP),
    ('valTestsElevenOrMoreP', valTestsElevenOrMoreP),
    ('tablePrecentageOfUsers', tablePrecentageOfUsers),
  ])

  x = list(numberOfRuns.keys())
  y = [numberOfRuns[k] for k in x]
  return {
    'data': [(x,y)],
    'method': 'bar',
    'xticks': [1,5,10]+list(numberOfRuns.keys())[-5:],
    'yticks': list(set(numberOfRuns.values()))[-3:],
    'xlabel': "Number of test run",
    'ylabel': "Number of users in category",
#    'table': {
#      'cellText': [(f"{x}:", y) for x,y in zip(x,y)],
#      'colLabels': ['Tests Run','#Users'],
#      'loc': 'upper right',
#      'colWidths': [0.15, 0.15],
#      'cellLoc': 'center',
#      'bbox': [0, -0.3, 1, 0.275],
#    },
#    'table_cell_height': 0.07,
  }
