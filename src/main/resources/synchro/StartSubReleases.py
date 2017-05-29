#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#


def new_variable_string(name, value):
    print "* new variable {0}->{1}".format(name, value)
    type = Type.valueOf('xlrelease.StringVariable')
    var = type.descriptor.newInstance(name)
    var.setValue(value)
    var.setKey(name)
    print "* var %s" % var
    print "* var %s" % type
    return var


def resolve_template(template):
    print "* resolve %s" % template
    search = templateApi.getTemplates(template)
    if len(search) == 0:
        raise Exception('Cannot resolve template {0}'.format(template))
    print search[0]
    return search[0].id


def add_task(title, template):
    print "* Create a new task %s -> %s " % (title, template)
    phase = getCurrentPhase()
    
    task = taskApi.newTask("xlrelease.CreateReleaseTask")
    task.title = "Start {0}".format(title)
    task.newReleaseTitle = title
    task.templateId = resolve_template(template)
    task.startRelease = True
    task.releaseTags = set([title])
    task.setTemplateVariables([new_variable_string('LR', getCurrentRelease().title)])
    taskApi.addTask(phase.id, task)


for key, value in subTasks.iteritems():
    print "-------------------------"
    add_task(key, value)
