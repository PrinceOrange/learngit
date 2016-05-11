# -*- coding: utf-8 -*-
# _author_='HAN'

import os
import const
from enum import Enum, unique


class Lz4StreamTInternal(object):
    hash_table = []
    # current_offset
    # init_check
    # dictionary
    # buffer_start
    # dict_size

class Lz4:
    def __init__(self, inputStr):
        self.inputStr = inputStr  # 输入流
        self.searchSize = 5    # 搜索缓冲区(已编码区)大小
        self.aheadSize = 3     # lookAhead缓冲区（待编码区）大小
        self.windSpiltIndex = 0  # lookHead缓冲区开始的索引
        self.move = 0
        self.notFind = -1   # 没有找到匹配字符串

    # 得到滑动窗口的末端索引
    def getWinEndIndex(self):
        return self.windSpiltIndex + self.aheadSize

    # 得到滑动窗口的始端索引
    def getWinStartIndex(self):
        return self.windSpiltIndex - self.searchSize

    # 判断lookHead缓冲区是否为空
    def isLookHeadEmpty(self):
        return True if self.windSpiltIndex + self.move > len(self.inputStr) - 1 else False

def compress(self):
        step = 0
        print("Step   Position   Match   Output")
        while not self.isLookHeadEmpty():
            # 1.滑动窗口
            self.winMove()
            # 2. 得到最大匹配串的偏移值和长度
            (offset, matchLen) = self.findMaxMatch()
            # 3.设置窗口下一步需要滑动的距离
            self.setMoveSteps(matchLen)
            if matchLen == 0:
                # 匹配为0，说明无字符串匹配，输出下一个需要编码的字母
                nextChar = self.inputStr[self.windSpiltIndex]
                result = (step, self.windSpiltIndex, '-',  '(0,0)' + nextChar)
            else:
                result = (step, self.windSpiltIndex, self.inputStr[self.windSpiltIndex - offset: self.windSpiltIndex - offset + matchLen], '(' + str(offset) + ',' + str(matchLen) + ')')
            # 4.输出结果
            self.output(result)
            step += 1        # 仅用来设置第几步

def winMove(self):
        self.windSpiltIndex = self.windSpiltIndex + self.move

    # 寻找最大匹配字符并返回相对于窗口分界点的偏移值和匹配长度
    def findMaxMatch(self):
        matchLen = 0
        offset = 0
        minEdge = self.minEdge() + 1  # 得到编码区域的右边界
        # 遍历待编码区，寻找最大匹配串
        for i in range(self.windSpiltIndex + 1, minEdge):
            offsetTemp = self.searchBufferOffest(i)
            if offsetTemp == self.notFind:
                return (offset, matchLen)
            offset = offsetTemp  # 偏移值

            matchLen = matchLen + 1  # 每找到一个匹配串，加1

        return offset, matchLen

    # 入参字符串是否存在于搜索缓冲区，如果存在，返回匹配字符串的起始索引
    def searchBufferOffest(self, i):
        searchStart = self.getWinStartIndex()
        searchEnd = self.windSpiltIndex
        # 下面几个if是处理开始时的特殊情况
        if searchEnd < 1:
            return self.notFind
        if searchStart < 0:
            searchStart = 0
            if searchEnd == 0:
                searchEnd = 1
        searchStr = self.inputStr[searchStart: searchEnd]  # 搜索区字符串
        findIndex = searchStr.find(self.inputStr[self.windSpiltIndex : i])
        if findIndex == -1:
            return -1
        return len(searchStr) - findIndex

    # 设置下一次窗口需要滑动的步数
    def setMoveSteps(self, matchLen):
        if matchLen == 0:
            self.move = 1
        else:
            self.move = matchLen

@unique
class LimitedOutputDirective(Enum):
    notLimited = 0
    limitedOutput = 1
table_type_t = Enum('table_type_t', ('byPtr', 'byU32', 'byU16'))
dict_directive = Enum('dict_directive', ('noDict', 'withPrefix64k', 'usingExtDict'))
dict_directive.noDict = 0
dictIssue_directive = Enum('dictIssue_directive', ('noDictIssue', 'dictSmall'))
dictIssue_directive.noDictIssue = 0


class EndConditionDirective(Enum):
    endOnOutputSize = 0
    endOnInputSize = 1


class EarlyEndDirective(Enum):
    full = 0
    partial = 1


const.memory_usage = 14
const.lz4_hash_log = 12
const.hash_table_size = 2 ^ 14
const.hash_size_u32 = 2 ^ 12
const.hash_nb_cells4 = 2 ^ 12

const.mini_match = 4
const.copy_length = 8
const.last_literals = 5
const.mf_limit = const.copy_length + const.mini_match
const.lz4_min_length = const.mf_limit + 1
const.lz4_max_input_size = 64 * (1 << 10)
const.lz4_64k_limit = 64 * (1 << 10) + const.mf_limit - 1
const.skipStrength = 6
const.prime_5bytes = 889523592379
const.ml_bits = 4
const.ml_mask = (1 << const.ml_bits) - 1
const.run_bits = 8 - const.ml_bits
const.run_mask = (1 << const.run_bits) - 1
const.max_d_log = 16
const.max_distance = (1 << const.max_d_log) - 1
# hash_table = []
# 判断系统为32位还是64位
prg = 'C:\Program Files (x86)'
if os.path.exists(prg) == 1:
    print("64bit")
    const.system_type_64 = 1
else:
    print("32bit")

file_name = input('Please Input the File name')
f = open('file_name', 'rb')

def lz4_hash_sequence32(sequence, table_type_t):
    if table_type_t == table_type_t.byU16:
        return (sequence * 2654435761) >> ((const.mini_match*8)-(const.lz4_hash_log+1))
    else:
        return (sequence * 2654435761) >> ((const.mini_match*8)-const.lz4_hash_log)


def lz4_hash_sequence64(sequence, table_type_t):
    if table_type_t == table_type_t.byU16:
        const.hash_log = (const.lz4_hash_log+1)
    else:
        const.lz4_hash_log
    const.hash_mask = (1 << const.hash_log) - 1
    ((sequence * const.prime_5bytes) >> (40 - const.hash_log)) & const.hash_mask


def lz4_hash_sequence_choose(sequence, table_type_t):
    if const.system_type_64 == 1:
        return lz4_hash_sequence64(sequence, table_type_t)
    else:
        return lz4_hash_sequence32(sequence, table_type_t)


def lz4_read_choose(p):
    if const.system_type_64 == 1:
        return lz4_read64(p)
    else:
        return lz4_read32(p)


def lz4_read64(p):
    pass


def lz4_read32(p):
    pass


def lz4_hash_position(p, table_type_t):
    return lz4_hash_sequence_choose(lz4_read_choose(p), table_type_t)


def lz4_put_position_on_hash(p, h, table_base, table_type_t, src_base):
    if table_type_t == byPtr:
        hash_table[0] = table_base
        hash_table[h] = p
        return
    # elif table_type_t == byU32:
    else:
        hash_table[0] = table_base
        hash_table[h] = p - src_base
        return


def lz4_put_position(p, table_base, table_type_t, src_base):
    h = lz4_hash_position(p, table_type_t)
    lz4_hash_position(p, h, table_base, table_type_t, src_base)


def lz4_get_position_on_hash(h, table_base, table_type_t, src_base):
    if table_type_t == byPtr:
        hash_table[0] = table_base
        return hash_table[h]
    # elif table_type_t == byU32:
    else:
        hash_table[0] = table_base
        return hash_table[h] + src_base


def lz4_get_position(p, table_base, table_type_t, src_base):
    h = lz4_hash_position(p, table_type_t)
    return lz4_get_position_on_hash(h, table_base, table_type_t, src_base)


# compress
def lz4_compress_generic(ctx, source, dest, input_size, max_output_size):
    const.ip = const.source
    # const BYTE* base;
    # const BYTE* lowLimit;
    # const BYTE* const lowRefLimit = ip - dictPtr->dictSize;
    # const BYTE* const dictionary = dictPtr->dictionary;
    # const BYTE* const dictEnd = dictionary + dictPtr->dictSize;
    # const size_t dictDelta = dictEnd - (const BYTE*)source;
    const.anchor = const.source
    const.iend = const.ip + inputSize
    const.mflimit = const.iend - const.mf_limit
    const.matchlimit = const.iend - const.last_literal
    op = dest
    const.olimit = op + max_output_size
    if input_size > lz4_max_input_size:
        return 0
    if dict == dict_directive.noDict:
        base = source
        lowlimit = source
    elif dict == dict_directive.withPrefix64K:
        base = source - dict.current_offset
        lowlimit = source - dict.dict_size
    elif dict == dict_directive.usingExtDict:
        base = source - dict.current_offset
        lowlimit = source
    if table_type_t == byU16 and (input_size >= const.lz4_64k_limit):
        return 0
    if input_size < const.lz4_min_length:
        last_literals()

# First Byte
    lz4_hash_position(ip, ctx, table_type_t, base)
    ip += 1
    forward_h = lz4_hash_position(ip, table_type_t)

    while True:
        find_match_attempts = (1 << const.skipStrength) + 3
        while True:
            h = forward_h
            find_match_attempts += 1
            step = find_match_attempts >> const.skipStrength
            ip = forward_ip
            forward_ip = ip + step
            if forward_ip > const.mf_limit:
                last_literals()
            forward_h = lz4_hash_position(forward_ip, table_type_t)
            ref = lz4_get_position_on_hash(ip, h, table_type_t, base)
            lz4_put_position_on_hash(ip, h, ctx, table_type_t, base)
            if (ref + const.max_distance > ip) and (LZ4_read32(ref+ref) == LZ4_read32(ip)):
                    break
    while (ip > const.anchor) and (ref > lowlimit) and (ip[-1] == ref[-1]):
        ip -= 1
        ref -= 1
    length = ip - anchor
    op += 1
    token = op
# check output limit
    if limited_output and (op + length + (2 + 1 + const.last_literal) + (length >> 8) > const.olimit):
        return 0
    if length >= const.run_mask:
        len = length - const.run_mask
        token = (const.run_mask << const.ml_bits)
        while len >= 255:
            len -= 255
            op += 255
    else:
        token = length << const.ml_bits
# copy literals
    end = op + length
    lz4_wild_copy(op, anchor, end)
    op = end
# 向后扩展未加入，未找到对应部分
#


def last_literals(iend, anchor, op, dest, limitedOutput):
    last_run = iend - anchor
    if limitedOutput and ((op - dest) + last_run + 1 + (last_run + 255 - const.run_mask) / 255 > maxOutputSize)
        return 0
    if last_run >= const.run_mask:
        accumulator = last_run - const.run_mask
        op += 1
        op = const.run_mask << const.ml_bits
        while accumulator >= 255:
            accumulator -= 255
            op +=255
        op += 1
        op = accumulator
    else:
        op += 1
        op = last_run
    return op - dest




