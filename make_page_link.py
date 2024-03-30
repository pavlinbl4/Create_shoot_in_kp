def make_page_link(shoot_id):
    shoot = shoot_id.split('_')
    return f"https://image.kommersant.ru/photo/wp/default.aspx?shootnum={shoot[1]}&sourcecode={shoot[0]}"


def make_history_link(first_link):
    inner_id = first_link.split('=')[1]
    return f'https://image.kommersant.ru/photo/archive/adm/ShootHistoryLog.aspx?id={inner_id}&insid=-{inner_id}'


def make_shoot_edit_link(link):
    shoot_edit_link = f'https://image.kommersant.ru/photo{link[2:]}'
    return shoot_edit_link
