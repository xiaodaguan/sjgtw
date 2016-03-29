# coding=utf-8

u = u"共37条数据"


utf = u.encode('utf-8')

sub = utf[utf.find("共")+3:utf.find("条")]
print(sub)