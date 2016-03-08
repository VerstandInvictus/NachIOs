import requests
import config
import json
requests.packages.urllib3.disable_warnings()

"""
this is a quick and dirty framework for mass-deleting nodes under a certain
parent, should you find yourself accidentally having added 327 completed tasks
for the same article when your Pocket checking script inexplicably encounters
a Pocket API object without a certain field - apparently, in the Pocket API,
any response object "may or may not contain the following information", and
after that they list every possible response field including item_id. It's
nice to have parameters you can depend on, isn't it?

It should be used via interactive console:
    >>> import config
    >>> import deletebyname
    >>> ptr = deletebyname.getNodesToIterate("pages")
    Found root node: Pages to Read
    >>> deletebyname.deleteNodesByName(ptr, "why romney asked republicans")
    deleted Why Romney Asked Republicans to Vote for Rubio. And Cruz. And Kasich.
    deleted Why Romney Asked Republicans to Vote for Rubio. And Cruz. And Kasich.
    deleted Why Romney Asked Republicans to Vote for Rubio. And Cruz. And Kasich.
    ... et cetera.
"""


def deleteNodesByName(inp, string):
    """
    Iterate tasks within our root node, deleting those that match our desired
    title.

    :param inp: the list of nodes from getNodesToIterate
    :param string: a string that appears in the name of each node you want to
    delete (doesn't need to be the full name, caps don't matter)
    :return none, it prints results
    """
    for each in inp:
        check = requests.get(
            'https://nachapp.com/api/nodes/' + str(each),
            auth=(config.nachApiKey, ''),
            verify=False)
        if string.lower() in json.loads(check.text)['name'].lower():
            delete = requests.delete(
                'https://nachapp.com/api/nodes/' + str(each),
                auth=(config.nachApiKey, ''),
                verify=False)
            print "deleted", json.loads(check.text)['name']


def getNodesToIterate(name):
    """
    Get IDs for all nodes in the root node that contains duplicates.

    I do NOT think the API call recursively crawls goals, so if one of the
    nodes listed is a goal, you won't get its child tasks. I haven't tested
    this, because I am not yet insane enough to programatically add sub-goals
    and sub-sub-tasks, so I don't have hundreds of duplicates spread across my
    entire goal map - thankfully they contained themselves to the top level of
    one root node.

    :param name: the name of the root-level node under which we have duplicate
    tasks (doesn't need to be the full name, caps don't matter, but it will
    return nodes for only the first match)
    :return: a list of all node IDs in the root-level node we found
    """
    testSearch = requests.get(
        'https://nachapp.com/api/users/' + str(config.nachUser) + "/nodes",
        auth=(config.nachApiKey, ''),
        verify=False)
    ptr = [(x['name'],
            x['id'],
            x['children']) for x in json.loads(testSearch.text)]
    for each in ptr:
        if name.lower() in each[0].lower():
            print "Found root node: {0}".format(each[0])
            return each[2]
