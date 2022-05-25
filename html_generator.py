from database import BaseDatabase
from utils import Utils
HEAD_CODE = """<br/><br/><br/>
<!DOCTYPE html>
<html>
 <head>
  <meta charset="utf-8">
<style>
  body
{
    font-size: 12pt;
    font-family: Calibri;
    padding : 10px;
}

table
{
    border: 1px solid black;

}
th
{
    border: 1px solid black;
    padding: 5px;
    background-color:grey;
    color: white;
    font-size: 34px;

}
td
{
    border: 1px solid black;
    padding: 5px;
    font-size: 34px;
}

input
{
    font-size: 12pt;
    font-family: Calibri;
}
</style>
</head>
<body>
<div id="dvData" class="container">
  <table class="table table-bordered">
      <tr>
          <th>Сумма</th>
          <th>Примечание</th>
          <th>Тип</th>
      </tr>
"""

END_CODE = """  </table>"""


class HtmlGenerator:
    def __init__(self):
        self.head_code = HEAD_CODE
        self.end_code = END_CODE
        self.db = BaseDatabase()
        self.utils = Utils()

    @staticmethod
    def parse_type(array):
        complete = []
        for i in array:
            if i[3] == 1:
                complete.append([i[2], "Зачисление", i[4]])
            else:
                complete.append([i[2], "Трата", i[4]])
        return complete

    def generation_code(self, telegram_id):
        array = self.parse_type(
            self.db.transactions_get(
                telegram_id=telegram_id))
        code = ""
        for i in array:
            code = code + f"""<tr>
                                  <td>{self.utils.locale_balance(i[0])}</td>
                                  <td>{i[2]}</td>
                                  <td>{i[1]}</td>
                             </tr>"""
        return self.head_code + code + self.end_code

    @staticmethod
    def generation_file(code):
        f = open("detalization.html", "w", encoding='utf-8')
        f.write(code)
        f.close()

    def generation(self, telegram_id):
        self.generation_file(self.generation_code(telegram_id=telegram_id))
        return "detalization.html"
