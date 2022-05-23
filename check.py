import xlrd
import xlwt
import xlutils.copy


def make_db(filename):
    """
    生成当日医院反馈数据库（支持xlsx和xls）
    :param filename:
    :return:
    """

    data = xlrd.open_workbook(filename)
    table = data.sheets()[0]
    nrows = table.nrows - 1

    db = {}
    for idx in range(1, nrows + 1):
        record = table.row(idx)
        uid = str(record[2].value)
        name = str(record[0].value)
        dt = str(record[7].value)

        db[uid] = (name, dt)

    return db


def write_ret(filename, db):
    """
    写入学校统计表格
    :param filename:
    :param db:
    :return:
    """
    success_count = 0
    fail_count = 0

    # 不在医院数据库中的记录
    not_in_db = []
    # 异常记录（如姓名不符）
    error_record = []

    # 标红样式
    error_style = xlwt.easyxf('pattern: pattern solid, fore_colour red')

    # 若为xlsx则不支持复制格式，xls支持
    if filename.split('.')[-1] == 'xlsx':
        rd = xlrd.open_workbook(filename)
    else:
        rd = xlrd.open_workbook(filename, formatting_info=True)
    wt = xlutils.copy.copy(rd)  # 复制一份

    # 创建表对象
    rd_table = rd.sheets()[0]
    wt_table = wt.get_sheet(0)
    nrows = rd_table.nrows - 1

    for idx in range(2, nrows + 1):
        record = rd_table.row(idx)
        name = str(record[4].value)
        uid = str(record[5].value)
        uid = uid.split('.')[0]  # 避免学号用数值类型的干扰

        # 获取db中对应记录，没有则记录
        if uid not in db.keys():
            not_in_db.append((idx + 1, uid, name))
            wt_table.write(idx, 9, '', error_style)
            fail_count += 1
        else:
            db_record = db[uid]
            # 校验姓名
            if not db_record[0] == name:
                error_record.append((idx + 1, uid, name))
                wt_table.write(idx, 9, '', error_style)
                fail_count += 1
            else:
                wt_table.write(idx, 9, db_record[1])
                success_count += 1

    wt.save(filename)

    return (not_in_db, error_record, success_count, fail_count)


if __name__ == "__main__":
    db = make_db('upload/检测信息0520(1).xlsx')
    print(write_ret('upload/XX学院-X月X日-XX人-50%核酸抽检学生名单.xls', db))
