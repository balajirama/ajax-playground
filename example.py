import my_utils

lofd = [{'num': 1}, {'num': 2}]

def act_link(larg):
    if len(larg) == 0:
        return ""
    return '<a href="/path/'+str(larg[0])+'">Path</a>'

print(my_utils.add_column_to_query_result(lofd, column='links', funcname=act_link, args=['num']))
print(lofd)
