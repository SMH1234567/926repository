import requests
from lxml import etree
import time
import multiprocessing
import pymysql

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    'cookie': '_zap=7e57c2da-00c7-4b66-94b3-4502369bd572; d_c0="AECZSZ_9OxKPTgxRnBwdve-s119Pmjc5pKE=|1606043553"; __snaker__id=HOhNadRzYTTZ7ddw; _9755xjdesxxd_=32; gdxidpyhxdE=2tMdZaC7ot6VjpyE94XKvJN2LBzNJts5BSrO%2FmyPDbAb6zraogipgrfEAS8NHJZIT16ShE8BgdjlughkUu%2B9Nd%2B2H4nLr%5C%2FG1HbR5p9NDcLhahzxwPCVUjBN4mp6vEHiNjsWqs0EMaMSB2U4MZmB2rE4qcUjXPPm1dcIGnvPLah%2BHbrS%3A1615889484133; YD00517437729195%3AWM_NI=p2oT0QL%2F44QM9HUw1rbQfxp0VHRHSeNTRYjAfvqt4TYddyTGJlQOhV1q%2FAXFqW1vRD79i5VkbdjpJDAP62JqHg6%2FIVpHiAlx5WiVE2Edu%2FxspHcmtwXFw3mBWV5ohMfzQ3g%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eeb6cc46b4ed9984c673a19a8fa6c84b879e8ebbae3c87afacacb23392b08dabd02af0fea7c3b92ab4eea1b5b35b90f1fcd5d447fb989b98b47aa28faa99f33c96989ea9d26f8e8c9ebae94ba6aabf95b7609bbcac9ad74d8ab49fb0eb5ef3afe1a2db4eb389ff97d150f5e7a7d6d561a2bca691c9508390fad3c97b8cb9fad0cc5eb498a7a2ef74f789a7b7c83a87bcbbd0fb79b498ad8ef77d9c9ab9d4f04a958afb90eb47a6a69fd4e637e2a3; YD00517437729195%3AWM_TID=ZkoI2i0ICxVAUVEEFAc60Fucf28V5HYJ; z_c0="2|1:0|10:1615888616|4:z_c0|92:Mi4xLVVUd0VRQUFBQUFBUUpsSm5fMDdFaVlBQUFCZ0FsVk42TTQ5WVFCc2FXS1AzOWQzNmJpSUZsLXhYVHFQT2Fqcjln|2cc088fc81ad46e077ccc4a6f676e23cab9d0dc035a07ccd2356e9383479365c"; Hm_lvt_eaa57ca47dacb4ad4f5a257001a3457c=1625388966,1625927006; _xsrf=35f6ab89-58f9-4b78-9ad4-ceaf345f17f3; tshl=; tst=h; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1625969319,1626077731,1626080239,1626273006; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1626273006;'
}
url = 'https://www.zhihu.com/hot'


def get_question_num(url, headers):
    response = requests.get(url, headers=headers)
    text = response.text
    html = etree.HTML(text)
    reslut = html.xpath("//section[@class='HotItem']")
    # 获取问题的ID
    question_list = []
    for question in reslut:
        number = question.xpath(".//div[@class='HotItem-index']//text()")[0].strip()
        title = question.xpath(".//h2[@class='HotItem-title']/text()")[0].strip()
        href = question.xpath(".//div[@class='HotItem-content']/a/@href")[0].strip()
        question_num = href.split('/')[-1]
        question_list.append([question_num, title])
        # print(number,'\n',title,'\n',href)
    return question_list


# 数据json请求（问题均通过ajax请求）
# 分析链接格式,如下:
# https://www.zhihu.com/api/v4/questions/359056618/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset=5&platform=desktop&sort_by=default
# 变化量如：question_id , offset=5,10,15......
def data_json_request(question_id, question_title, headers):
    num = 0
    i = 1
    while True:
        json_url = 'https://www.zhihu.com/api/v4/questions/' + question_id + '/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset={}&platform=desktop&sort_by=default'.format(
            num)
        data_json = requests.get(json_url, headers=headers)
        all_detail_data = data_json.json()['data']
        length_detail_data = len(all_detail_data)
        for one_detail_data in all_detail_data:
            question_title = question_title
            answer_author = one_detail_data['author']['name']
            author_introduce = one_detail_data['author']['headline']
            author_followers = one_detail_data['author']['follower_count']
            answer_vote_num = one_detail_data['voteup_count']
            answer_comment_num = one_detail_data['comment_count']
            updated_time = one_detail_data['updated_time']
            content = one_detail_data['content']
            # 保存数据至数据库
            db = pymysql.connect(host='localhost', user='root', password='926926', port=3306, db='spider_data')
            cursor = db.cursor()
            sql = 'INSERT INTO zhihu_hot_question(question_title,author_name,author_introduce,author_followers,answer_vote_num,answer_comment_num,updated_time,content) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'
            try:
                if int(answer_vote_num) >= 90:
                    cursor.execute(sql, (
                    question_title, answer_author, author_introduce, author_followers, answer_vote_num,
                    answer_comment_num, updated_time, content))
                    db.commit()
                    print('数据写入成功！！！')
                else:
                    print('点赞数太少，不保存至数据库！！！')
            except:
                print('数据写入失败！')
                db.rollback()
            # print(question_title,'\n',answer_author,'\n',author_introduce,'\n',author_followers,'\n',answer_vote_num,'\n',answer_comment_num
            # ,'\n',updated_time,'\n',content)
        num = i * 5
        i = i + 1
        if length_detail_data == 0:
            print('answaer_stop!!!!!')
            break


# def save_to_mysql():
#     db = pymysql.connect(host='localhost',user='root',password='123456',port=3306,db='spider_data')
#     cursor = db.cursor()
#     sql = 'INSERT INTO zhihu_hot_question(question_title,author_name,author_introduce,author_followers,answer_vote_num,answer_comment_num,updated_time,content) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'


def main():
    question_id = get_question_num(url, headers)
    print(question_id)
    print('当前环境CPU核数是：{}核'.format(multiprocessing.cpu_count()))
    p = multiprocessing.Pool(4)
    for q_id in question_id:
        p.apply_async(data_json_request, args=(q_id[0], q_id[1], headers))
    p.close()
    p.join()


if __name__ == "__main__":
    start = time.time()
    main()
    print('总耗时：%.5f秒' % float(time.time() - start))