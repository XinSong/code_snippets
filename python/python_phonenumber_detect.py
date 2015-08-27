#coding=gbk
import sys

sys.path.append('apl')
sys.path.append('lib')
sys.path.append('conf')

import re
import json

class UrlIdentifier:
    def __init__(self):
        # ��ȷ
        self.url_pattern = re.compile(r'(([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6})')
        # ����
        self.suspect_pattern = re.compile(r'([a-zA-Z0-9]([0-9a-zA-Z][^0-9a-zA-Z-]{,2}){4,})[a-zA-Z0-9]') # �Ա�׼���ſ�ͷ�ͽ�β���м��������2�������ַ����ܳ��Ȳ�С��6

    def match(self, content):
        url = ''
        suspect_url = ''

        match = self.url_pattern.search(content)
        if match:
            url = match.group(0)

        if not url:
            match = self.suspect_pattern.search(content)
            if match:
                suspect_url = match.group(0)

        return url, suspect_url


class TeleIdentifier:

    def __init__(self):
        # ���Ƶ绰
        self.suspect_pattern_list = [
            re.compile(r'(([0-9]){6,11}[0-9])'), # ����ƥ��������
            re.compile(r'(([0-9]-?){6,11}[0-9])'), # ƥ���м���-��
            re.compile(r'(([0-9] ?){6,11}[0-9])'), # ƥ���м��пո��
        ]

        # ���Ƶ绰������
        self.white_list_pattern = [
            re.compile(r'20[01][0-9]')
        ]

        # �ֻ����ʽ
        self.mobile_pattern_list = [
            re.compile(r'(^1[0-9]{3}[- ]?[0-9]{3}[- ]?[0-9]{4})$'),  # ��ʽ��1381 111 2222��1381-111-2222
            re.compile(r'(^1[0-9]{2}[- ]?[0-9]{4}[- ]?[0-9]{4})$'),  # ��ʽ��138 1111 2222��138-1111-2222
            re.compile(r'(^1[0-9]{3}[- ]?[0-9]{4}[- ]?[0-9]{3})$'),  # ��ʽ��1381 1111 222��1381-1111-222
            re.compile(r'(^1 ?([0-9] ){9}[0-9])$'),                 # ��ʽ��1 3 8 1 1 1 1 1 2 2 2
        ]

        # ��;�绰
        from phone_area_conf import AREA_CODE_LIST
        self.area_codes = set(AREA_CODE_LIST)
        self.long_distance_pattern_list = [
            re.compile(r'^(([0-9]{3,4})[- ]?[0-9]{4}[- ]?[0-9]{3,4})$'),  # ��ʽ�� 010-6688-8788
            re.compile(r'^(([0-9]{3,4})[- ]?[0-9]{3}[- ]?[0-9]{4,5})$'),  # ��ʽ�� 010-668-88788
        ]

        # 400, 800�绰
        self.special_pattern_list = [
            re.compile(r'^([48]00[- ]?([0-9][- ]?){6}[0-9])$')    # 400��800���7λ����
        ]

        # ����ʾ��ĵ绰���漰���ı���ʹ��unicode
        self.prompt_pattern_list = [
            re.compile(u'((�绰|����|����|С��|Ůʿ|�µ�|��ϵ)[^0-9]{0,6}(([0-9][- ]?){9,11}[0-9]|([0-9][- ]?){6,7}[0-9]))'),
            re.compile(u'((([0-9][- ]?){9,11}[0-9]|([0-9][- ]?){6,7}[0-9])[^0-9]{0,6}(����|Ůʿ|С��))'),
        ]


    def match(self, content):
        numbers = self.mainly_match(content)
        match_number = ""
        if numbers:
            match_number = self.contain_mobile_number(numbers)
            if match_number:
                return numbers, match_number
            match_number = self.contain_long_distance_number(numbers)
            if match_number:
                return numbers, match_number
            match_number = self.contain_special_number(numbers)
            if match_number:
                return numbers, match_number
            match_number = self.contain_promted_number(content)
            if match_number:
                return numbers, match_number

        return numbers, match_number


    def mainly_match(self, content):
        '''
        @brief ȡ���ı����������Ƶ绰����
        @param content �ı�
        @return ���ƺ����б�
        '''
        match = False
        match_groups = set()
        # ȡ�����п��ɲ���
        for pattern in self.suspect_pattern_list:
            match_list = pattern.findall(content)
            if match_list:
                for groups in match_list:
                    number = groups[0]
                    if number not in match_groups:
                        match_groups.add(number)

        white_groups = set()
        # ������ɸѡ
        for group in match_groups:
            for pattern in self.white_list_pattern:
                white = pattern.search(group)
                if white:
                    white_groups.add(group)


        return list(match_groups - white_groups)


    def contain_mobile_number(self, numbers):
        match_number = ""
        for number in numbers:
            for pattern in self.mobile_pattern_list:
                match = pattern.search(number)
                if match:
                    match_number = match.group(0)
                    break

        return match_number

    def contain_long_distance_number(self, numbers):
        match_number = ""
        for number in numbers:
            for pattern in self.long_distance_pattern_list:
                if pattern.search(number) and (number[0:3] in self.area_codes or number[0:4] in self.area_codes):
                    match_number = number
                    break

        return match_number

    def contain_special_number(self, numbers):
        match_number = ""

        for number in numbers:
            for pattern in self.special_pattern_list:
                match = pattern.search(number)
                if match:
                    match_number = match.group(0)
                    break

        return match_number

    def contain_promted_number(self, content):
        match_number = ""

        for pattern in self.prompt_pattern_list:
            match = pattern.search(content.decode('gbk'))
            if match:
                match_number = match.group(0)
                break

        return match_number.encode('gbk')


class TencentIdentifier:
    def __init__(self):
        self.qq_pattern_list = [
            re.compile(u'(([qQ]{1,2})[^0-9]{0,6}[0-9]{5,})')
        ]

        self.weixin_pattern_list = [
            re.compile(u'((΢��|weixin)[^0-9a-zA-Z]{0,6}[a-zA-Z0-9][a-zA-Z0-9_-]{4,})')
        ]

    def match(self, content):
        match_account = ""
        for pattern in self.qq_pattern_list:
            match = pattern.search(content.decode('gbk'))
            if match:
                match_account = match.group(0)
                break

        for pattern in self.weixin_pattern_list:
            match = pattern.search(content.decode('gbk'))
            if match:
                match_account = match.group(0)
                break

        return match_account.encode('gbk')

def identify_tencent(content_pos = 0):
    identifier = TencentIdentifier()
    for line in sys.stdin:
        table = line.strip('\t').split('\t')
        if len(table) > content_pos:
            content = table[content_pos]
            match_account = identifier.match(content)
            print "%s\t%s" % (line.strip('\n'), match_account)
        else:
            print >> sys.stderr, "line=%s" % (line.strip('\n'))


def identify_url(content_pos = 0):
    identifier = UrlIdentifier()
    for line in sys.stdin:
        table = line.strip('\n').split('\t')
        if len(table) > content_pos:
            content = table[content_pos]
            match_url, suspect_url = identifier.match(content)
            print "%s\t%s\t%s" % (line.strip('\n'), match_url, suspect_url)
        else:
            print >> sys.stderr, "line=%s" % (line.strip('\n'))


def identify_tele(content_pos = 0):
    identifier = TeleIdentifier()
    for line in sys.stdin:
        table = line.strip('\t').split('\t')
        if len(table) > content_pos:
            content = table[content_pos]
            numbers, exact_number = identifier.match(content)
            if not numbers:
                numbers = ""
            else:
                numbers = numbers[0]
            print "%s\t%s\t%s" % (line.strip('\n'), numbers, exact_number)
        else:
            print >> sys.stderr, "line=%s" % (line.strip('\n'))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "usage: %s url|tele [textpos]"

    content_pos = 0
    if len(sys.argv) == 3:
        content_pos = int(sys.argv[2])

    ad_type = sys.argv[1]

    if ad_type == "url":
        identify_url(content_pos)
    elif ad_type == 'tele':
        identify_tele(content_pos)
    else:
        identify_tencent(content_pos)
