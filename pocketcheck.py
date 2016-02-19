import pocket
import config
import pprint

p = pocket.Pocket(config.consumerKey, config.accessToken)

articleList = p.get(detailType="simple", state="archive")

for each in articleList[0]['list'].itervalues():
    buildup = ' '
    for title in(
            each['resolved_title'],
            each['given_title'],
            each['resolved_url']):
        if len(title) == 0:
            pass
        else:
            print title
            break
