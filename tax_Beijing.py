#!/usr/bin/python
#coding=utf-8

import os,sys,re

#(start, end, ratio, fastleft)
tax_ratio = [(0, 36000, 0.03, 0), (36000, 144000, 0.1, 2520), (144000, 300000, 0.2, 16920), (300000, 420000, 0.25, 31920), (420000, 660000, 0.3, 52920), (660000, 960000, 0.35, 85920), (960000, -1, 0.45, 181920)]

if len(sys.argv) != 2 or ('-' not in sys.argv[1] and '+' not in sys.argv[1]):
    print 'Please Input Your Monthly Salary Like This : 月薪-专项扣除数+年终奖'
    exit(-1)

#获取工资信息
index_deduct=sys.argv[1].index('-')
index_bonus=sys.argv[1].index('+')
index_stock=sys.argv[1].index('++')
salary = int(sys.argv[1][:index_deduct])
deduct = int(sys.argv[1][index_deduct+1:index_bonus])
bonus  = int(sys.argv[1][index_bonus+1:index_stock])
stock  = int(sys.argv[1][index_stock+2:])

#税前扣除
fund         = 0.12
insurance    = fund + 0.102
starttax     = 5000

total_tax    = 0
total_deduct = 0
total_salary = 0

#获取对应税率
def get_proper_ratio(money):
    for r in tax_ratio:
        if money > r[0] and money <= r[1]:
            return r
    return tax_ratio[-1]

def print_one_line(l):
    length = 10
    s=''
    for item in l:
        try:
            stritem = re.sub(r"(?<=\d)(?=(?:\d\d\d)+$)", ",", item.decode('utf-8'))
            if '->' in stritem:
                s += stritem.center(4)
            else:
                s += stritem.center(length)
        except:
            stritem = item.decode('utf-8')
            s += stritem
    print s

def print_header():
    print ''.center(140,'-')

def calc_month_tax(income, before_tax):
    if income > 0:
        r = get_proper_ratio(income)
        month_tax = income * r[2] - r[3] - total_tax
    else:
        r = (0, 0, 0, 0)
        month_tax = 0
    return (r, month_tax)

print_header()
print '                                  2019年北京市个人所得税计算方法（税前月薪为 %d，年终奖为%d, 股票为%d）'%(salary, bonus, stock)
print_header()
print "            应纳税额  ->  五险一金   起征点   专项扣除  适用税率    纳税    ->  到手工资  公积金    ->  年终奖  合并扣税  单独计税     股票"
month_tax=0
month_insurance=salary * insurance
if month_insurance > 5639.02:
    month_insurance = 5639.02
month_fund=salary * fund * 2
if month_fund > 6096.24:
    month_fund = 6096.24

m=1
while m <= 12:
    total_salary = m * salary
    total_deduct = m * deduct
    total_insurance    = m * month_insurance

    (r, month_tax) = calc_month_tax(total_salary-total_insurance-total_deduct-starttax*m, total_tax)
    #年终奖的两种计算方法
    if m == 12:
        month_bonus = bonus
        month_stock = stock

        #合并扣税
        (merge_bonus_r, merge_bonus_tax) = calc_month_tax(total_salary+bonus-total_insurance-total_deduct-starttax*m, total_tax)
        merge_bonus_tax -= month_tax

        #单独计税
        alone_bonus_r = get_proper_ratio(bonus)
        alone_bonus_tax = bonus * alone_bonus_r[2] - (alone_bonus_r[3]/12)

        #股票单独计税
        alone_stock_r = get_proper_ratio(stock)
        alone_stock_tax = stock * alone_stock_r[2] - (alone_stock_r[3])
    else:
        month_bonus = 0
        merge_bonus_tax = 0
        alone_bonus_tax = 0
        month_stock = 0
        alone_stock_tax =0

    total_tax += month_tax
    print_one_line(["%.f月"%(m), "%.f"%(salary), "->", "%.f"%(month_insurance), "%.f"%(starttax), "%.f"%(deduct), "%.f%%"%(r[2]*100), "%.f"%(month_tax), "->", "%.f"%(salary - month_tax-month_insurance), "%.f"%(month_fund), "->", "%.f"%(month_bonus), "%.f"%(month_bonus-merge_bonus_tax), "%.f"%(month_bonus-alone_bonus_tax), "%.f"%(month_stock-alone_stock_tax)])
    m += 1

#判断合并扣税和单独计税哪种更好
if merge_bonus_tax > alone_bonus_tax:
    merge_good = ''
    alone_good = 'Good'
elif merge_bonus_tax < alone_bonus_tax:
    merge_good = 'Good'
    alone_good = ''
else:
    merge_good = 'Good'
    alone_good = 'Good'

print_header()
print_one_line(['总',"%.f"%(total_salary),"->", "%.f"%(month_insurance*12), "%.f"%(starttax*12), "%.f"%(total_deduct), "%.f%%"%(r[2]*100), "%.f"%(total_tax),"->","%.f"%(total_salary-total_tax-total_insurance), "%.f"%(month_fund*12), '->', '', merge_good, alone_good])
