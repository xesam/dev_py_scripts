# coding=utf-8


import os
import sys
import time

_base = "base"
_common_param = "common_param"
_common_method = "common_method"

_target = "target"
_desc = "desc"
_action = "action"
_param = "param"
_response = "response"
_eg = "eg"


class Form:
    def __init__(self):
        self.base = ""
        self.commons = []
        self.target = []
        self.desc = []
        self.action = []
        self.method = "get"
        self.param = []
        self.response = []
        self.eg = []

    def base_url(self, base):
        self.base = base

    def method(self, base):
        self.base = base

    def common_params(self, commons):
        self.commons = commons

    def get_format_target(self):
        return "".join(self.target)

    def get_format_desc(self):
        return "".join(self.desc)

    def get_format_action(self):
        return "".join([self.base + action for action in self.action])

    def get_format_param(self):
        return [p.split("#") for p in self.param] + [p.split("#") for p in self.commons]

    def get_format_response(self):
        return [p.split("#") for p in self.response]

    def get_format_eg(self):
        return "".join(self.eg)


class FormHtml:
    html_t = """
<!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8"/>
        <title>接口说明</title>
        <link rel="stylesheet" href="interface_doc.css"/>
    </head>
    <body>
    <div id="cll_frame_container">
    {k_time}
    {k_sections}
    </div>
</body>
</html>"""

    time_t = """
    <header class="doc_time">
        <h3>更新时间：{k_time}</h3>
    </header>"""

    section_t = """
    <section>
        {k_target}
        {k_desc}
        {k_param}
        {k_response}
        {k_eg}
    </section>"""

    target_t = """
    <header class="target">
        <h3>{k_content}</h3>
    </header>"""

    desc_t = """
    <div class="desc">
        <p>{k_content}</p>
    </div>"""

    param_t = """
    <form class="param" action="{k_action}">
        {k_content}
        <div><input type="submit" value="提交"/></div>
    </form>"""

    param_item_t = """
        <div><label>{k_name}</label><input type="text" name="{k_name}"/><span>{k_name_desc}</span></div>"""

    response_t = """
    <div class="response">
        <p>结果说明</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>描述</th>
            </tr>
            </thead>
            <tbody>
            {k_content}
            </tbody>
        </table>
    </div>"""

    response_item_t = """
    <tr>
        <td>{k_name}</td>
        <td>{k_name_desc}</td>
    </tr>"""

    eg_t = """
    <div class="eg"><p>结果示例</p><p>{k_content}</p></div>"""

    def __init__(self, forms):
        self.forms = forms

    def to_html(self):
        return self.html_t.format(k_time=self._render_time(), k_sections=self._render_section())

    def _render_time(self):
        return self.time_t.format(k_time=time.ctime())

    def _render_section(self):
        fragments = []
        for form in self.forms:
            fragments.append(self._render_section_item(form))
        return "".join(fragments)

    def _render_section_item(self, form):
        return self.section_t.format(
            k_target=self._render_target(form),
            k_desc=self._render_desc(form),
            k_param=self._render_param(form),
            k_response=self._render_response(form),
            k_eg=self._render_eg(form))

    def _render_target(self, form):
        return self.target_t.format(k_content=form.get_format_target())

    def _render_desc(self, form):
        return self.desc_t.format(k_content=form.get_format_desc())

    def _render_param(self, form):
        fragments = []
        for param in form.get_format_param():
            fragment = self._render_param_item(param)
            fragments.append(fragment)
        return self.param_t.format(k_action=form.get_format_action(), k_content="".join(fragments))

    def _complete(self, lst, d_len):
        if len(lst) == d_len:
            return lst
        else:
            return lst + ["" for p in range(d_len - len(lst))]

    def _render_param_item(self, pair):
        pair = self._complete(pair, 2)
        return self.param_item_t.format(k_name=pair[0], k_name_desc=pair[1])

    def _render_response(self, form):
        fragments = []
        for response in form.get_format_response():
            fragment = self._render_response_item(response)
            fragments.append(fragment)
        return self.response_t.format(k_content="".join(fragments))

    def _render_response_item(self, pair):
        pair = self._complete(pair, 2)
        return self.response_item_t.format(k_name=pair[0], k_name_desc=pair[1])

    def _render_eg(self, form):
        return self.eg_t.format(k_content=form.get_format_eg())


class Loader:
    def __init__(self):
        pass

    @staticmethod
    def _extract_attr(attr_line):
        return attr_line.replace("#", "")

    @staticmethod
    def _check_extract(extract):
        return extract

    def load_forms(self, filename):
        with open(filename) as _file:
            forms = []
            form = None
            extract = None
            base = []
            common_params = []
            common_method = None
            for line in _file:
                line = line.strip()
                if len(line) == 0:
                    continue
                if line.startswith("#"):
                    extract = Loader._extract_attr(line)
                    if extract == _target:
                        form = Form()
                        form.base_url("".join(base))
                        form.common_params(common_params)
                        forms.append(form)
                else:
                    if extract == _base:
                        base.append(line)
                    elif extract == _common_param:
                        common_params.append(line)
                    elif extract == _common_method:
                        common_method = extract
                    elif Loader._check_extract(extract):
                        getattr(form, extract).append(line)
            return forms


if __name__ == "__main__":
    args = sys.argv
    input_file_path = os.path.abspath(args[1])
    output_file_path = os.path.abspath(args[2])
    loader = Loader()
    fs = loader.load_forms(input_file_path)
    fsHtml = FormHtml(fs)
    with open(output_file_path, 'w') as _file:
        _file.write(fsHtml.to_html())
    pass
