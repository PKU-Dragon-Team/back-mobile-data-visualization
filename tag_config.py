#!/usr/bin/env python
# encoding: utf-8

from collections import Counter


tag_whitelist = set([x.split(':')[0] for x in open('top100.tags.txt', encoding='utf_8').readlines()])

tag_blacklist = set(['地名地址信息', '交通地名',
                     '路口名', '热点地名', '桥', '区县级地名',
                     '普通地名', '出入口', '楼栋号',
                     '高速路入口', '门牌信息', '工厂'])

tag_convertlist = {
    '村庄级地名': '村庄',
    '商务住宅': '商务写字楼',
    '住宅区': '住宅小区',
    '宿舍': '住宅小区',
    '商住两用楼宇': '商务写字楼',
    '出版社': '科教文化服务',
    '楼宇': '商务写字楼',
    '综合医院': '医疗保健服务',
    '经济型连锁酒店': '宾馆酒店',
    '传媒机构': '公司企业',
    '中餐厅': '餐饮服务',
    '购物服务相关': '购物服务',
    '产业园区': '公司企业',
    '网络科技': '公司企业',
    '汽车维修': '汽车相关',
    '汽车销售': '汽车相关',
    '大众特约维修': '汽车相关',
    '地铁站': '交通设施服务',
    '长途汽车站': '交通设施服务',
    '综合酒楼': '餐饮服务',
    '别墅': '住宅小区',
    '旅馆招待所': '宾馆酒店',
    '快餐厅': '餐饮服务',
    '普通商场': '购物服务',
    '服装鞋帽皮具店': '购物服务',
    '咖啡厅': '餐饮服务',
    '外国餐厅': '餐饮服务',
    '火车站': '交通设施服务',
    '驾校': '其他',
    '餐饮相关场所': '餐饮服务',
    '娱乐场所': '休闲娱乐',
    '影剧院': '休闲娱乐',
    '休闲场所': '休闲娱乐',
    '糕饼店': '餐饮服务',
    '清真菜馆': '餐饮服务',
    '餐饮相关': '餐饮服务',
    '服务区': '餐饮服务',
    '特色商业街': '休闲娱乐',
    '茶艺馆': '餐饮服务',
    '海鲜酒楼': '餐饮服务',
    '火锅店': '餐饮服务',
    '四川菜(川菜)': '餐饮服务',
    '公司': '公司企业',
    '知名企业': '公司企业',
    '住宿服务': '宾馆酒店',
    '度假疗养场所': '宾馆酒店',
    '四星级宾馆': '宾馆酒店',
    '五星级宾馆': '宾馆酒店',
    '三星级宾馆': '宾馆酒店',
    '旅馆招待所': '宾馆酒店',
    '住宿服务相关': '宾馆酒店',
    '科教文化场所': '科教文化服务',
    '美术馆': '科教文化服务',
    '展览馆': '科教文化服务',
    '高等院校': '科教文化服务',
    '特色/地方风味餐厅': '餐饮服务',
    '经济型连锁酒店': '餐饮服务',
    '区县级政府及事业单位': '政府机构及社会团体',
    '工商税务机构': '政府机构及社会团体',
    '政府机关': '政府机构及社会团体',
    '省直辖市级政府及事业单位': '政府机构及社会团体',
    '交通车辆管理': '政府机构及社会团体',
    '公检法机构': '政府机构及社会团体',
    '幼儿园': '科教文化服务',
    '小学': '科教文化服务',
    '文化宫': '科教文化服务',
    '学校': '科教文化服务',
    '档案馆': '科教文化服务',
    '会展中心': '科教文化服务',
    '培训机构': '科教文化服务',
    '图书馆': '科教文化服务',
    '科研机构': '科教文化服务',
    '博物馆': '科教文化服务',
    '职业技术学校': '科教文化服务',
    '专营店': '购物服务',
    '专卖店': '购物服务',
    '家电电子卖场': '购物服务',
    # '社会团体': '社会团体',
    '金融保险机构': '金融业',
    '金融保险服务机构': '金融业',
    '银行': '金融业',
    '超级市场': '购物服务',
    '综合医院': '医疗保健服务',
    '专科医院': '医疗保健服务',
    '医药保健销售店': '医疗保健服务',
    '卫生院': '医疗保健服务',
    # '住宅小区': '住宅区',
    '家居建材市场': '购物服务',
    '综合市场': '购物服务',
    '普通商场': '购物服务',
    '商场': '购物服务',
    '公园': '体育休闲服务',
    '公园广场': '体育休闲服务',
    '运动场馆': '体育休闲服务',
}


def raw2dict(raw):
    if raw:
        tag_dict = dict([(x.split(':')[0],
                                       float(x.split(':')[1])) for x in raw.split(' ')])
    else:
        tag_dict = {'其他': 1}

    return tag_dict


def _clean_tags(tag_dict):
    for tag in tag_blacklist:
        tag_convertlist[tag] = '其他'

    for k, v in list(tag_convertlist.items()):
        if k not in tag_dict:
            continue

        if v in tag_dict:
            tag_dict[v] = tag_dict[v] + tag_dict[k]
        else:
            tag_dict[v] = tag_dict[k]

        del tag_dict[k]

    for tag in list(tag_dict.keys()):
        if tag not in tag_whitelist:
            v = '其他'
            if v in tag_dict:
                tag_dict[v] = tag_dict[v] + tag_dict[tag]
            else:
                tag_dict[v] = tag_dict[tag]

            del tag_dict[tag]

    if not len(tag_dict):
        tag_dict['其他'] = 1


def clean_tags(raw, n=5):
    tag_dict = raw2dict(raw)
    tag_dict = dict(Counter(tag_dict).most_common()[:n])
    _clean_tags(tag_dict)
    return tag_dict
