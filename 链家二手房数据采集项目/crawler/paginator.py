from config import logger,LJ_BASE_URL

def get_next_url(CURRENT_PAGE):
    url = LJ_BASE_URL + f'pg{CURRENT_PAGE}'
    return url

def has_nex_url(html,CURRENT_PAGE):
    '''判断是否还有下一页'''
    if not html:
        return False
    from lxml import etree
    tree = etree.HTML(html)
    try:
        no_results = tree.xpath('//div[@class="m-noresult"]/text()')[0]
    except:
        no_results = None
        pass
    if no_results == "未找到符合所选条件的二手房源，建议您调整筛选条件再试试":
        return False
    elif not no_results:
        pass

    if CURRENT_PAGE < 35:
        return True

    