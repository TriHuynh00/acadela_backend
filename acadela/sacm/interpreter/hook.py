from acadela.sacm.case_object.http_hook import HttpTrigger
from acadela.sacm import util

def interpret_case_hook(hookObj):
    return {
        "event": hookObj.event,
        "url": hookObj.url
    }

def interpret_http_hook(httpHookObj):
    return HttpTrigger(str.upper(httpHookObj.event),
                       httpHookObj.url,
                       str.upper(httpHookObj.method),
                       httpHookObj.failureMessage)

def sacm_compile(hookList):

    hooklistJson = []

    for hook in hookList:
        hookJson = {'$': {}}

        hookJsonAttr = hookJson['$']

        print('hook in task is {}', vars(hook))
        util.compile_attributes(hookJsonAttr, hook,
            ['on', 'url', 'method', 'failureMessage'])

        hooklistJson.append(hookJson)

    return hooklistJson
