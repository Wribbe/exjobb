from msccls.figures.utils import get_db, dump_vars, as_percent
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
  valTestsFiveToTen = 0
  valTestsElevenOrMore = 0
  numUsers = len(users)
  valTestNoTests = numUsers - valNumAnyTestsRun
  for numRuns, numUsers in numberOfRuns.items():
    if 5 >= numRuns <= 9:
      valTestsFiveToTen += numUsers
    elif numRuns > 9:
      valTestsElevenOrMore += numUsers

#  valNumAnyTestsRunP = valNumAnyTestsRun/numUsers
#  valNumFiveOrMoreTestRunP = valNumFiveOrMoreTestRun/numUsers

  # Convert to latex formatted percentages.
#  valNumAnyTestsRunP = asPercent(valNumAnyTestsRunP)
#  valNumFiveOrMoreTestRunP = asPercent(valNumFiveOrMoreTestRunP)

  dump_vars([
    ('valNumAnyTestsRun', valNumAnyTestsRun),
    ('valTestsFiveToTen', valTestsFiveToTen),
    ('valTestsElevenOrMore', valTestsElevenOrMore),
    ('valTestNoTests', valTestNoTests),
#    ('valNumAnyTestsRunP', valNumAnyTestsRunP),
  ])

  x = list(numberOfRuns.keys())
  y = list(numberOfRuns.values())
  return {
    'data': [(x,y)],
    'method': 'bar',
    'xticks': [1,5,10]+list(numberOfRuns.keys())[-3:],
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
