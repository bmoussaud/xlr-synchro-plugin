#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from com.xebialabs.xlrelease.api.v1.forms import Condition


def add_gate_task(title, env):
    print "* Create a new  gate with {0} title".format(title)
    phase = getCurrentPhase()
    current_task = getCurrentTask()
    task = taskApi.newTask("xlrelease.GateTask")
    task.title = title
    task.pythonScript.xldeployServer = current_task.getPythonScript().getProperty("xldeployServer")
    task.pythonScript.deploymentPackage = version
    task.pythonScript.environment = env
    task.pythonScript.displayStepLogs = False
    taskApi.addTask(phase.id, task)


def get_gate_task(task_name):
    search = taskApi.searchTasksByTitle(task_name, None, release.id)
    if len(search) == 0:
        raise Exception("* ERROR: No tasks with '{0}' title in this release".format(task_name))
    return search[0]


def new_dependency(release_name, phase_name, task_name):
    print "* Dependency is %s/%s/%s" % (release_name, phase_name, task_name)
    if len(releaseApi.searchReleasesByTitle(release_name)) == 0:
        raise Exception("* ERROR: the'{0}' release not found".format(release_name))

    master_release = releaseApi.searchReleasesByTitle(release_name)[0]

    result = taskApi.searchTasksByTitle(task_name, phase_name, master_release.id)
    if len(result) == 0:
        raise Exception(
            "* ERROR: No tasks with '{0}' title in the '{1}' phase in the '{2}' release".format(task_name, phase_name,
                                                                                                release_name))
    target = result[0]
    return target


task = get_gate_task(gateTaskName)
print "* Gate task is %s" % task.title
target = new_dependency(masterReleaseName, masterPhaseName, masterTaskName)
taskApi.addDependency(task.id, target.id)

if addAConditionInTheMasterRelease:
    condition = Condition()
    condition.title = "Check If the '%s' release is ready" % release.title
    if len([i for i in target.conditions if i.title == condition.title]) > 0:
        print "* '%s' is already in the conditions" % condition.title
    else:
        print "* add the '%s' in the condition condition" % condition.title
        taskApi.addCondition(target.id, condition)

generateGateCheckTask = False
groupName = 'Check All the deployments are ok'
if generateGateCheckTask:
    print '* Generate Gate Check Task {0}/{1}/{2}'.format(masterReleaseName, masterPhaseName, groupName)
    group_id = new_dependency(masterReleaseName, masterPhaseName, groupName)
    print group_id
    raise Exception('X')
    search = taskApi.searchTasksByTitle(groupName, None, release.id)

print "* Done"