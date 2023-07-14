from allib.testing import mock
from allib.sqla import Paginator


def test_paginator_does_not_call_offset_when_page_eq_1():
    query = mock.Mock()
    query.count = mock.Mock(return_value=500)
    query.offset = mock.Mock(return_value=query)
    query.limit = mock.Mock(return_value=query)
    query.all = mock.Mock(return_value=[])
    Paginator(query, 1, "http://localhost")
    query.offset.assert_not_called()
    query.limit.assert_called_once_with(50)
    query.all.assert_called_once_with()


def test_paginator_calls_offset_when_page_gt_1():
    query = mock.Mock()
    query.count = mock.Mock(return_value=500)
    query.offset = mock.Mock(return_value=query)
    query.limit = mock.Mock(return_value=query)
    query.all = mock.Mock(return_value=[])
    Paginator(query, 2, "http://localhost")
    query.offset.assert_called_once_with(50)
    query.limit.assert_called_once_with(50)
    query.all.assert_called_once_with()


def test_paginator_preserves_qs():
    query = mock.Mock()
    query.count = mock.Mock(return_value=500)
    paginator = Paginator(query, 5, "http://localhost?s=askdljf")
    assert paginator.url_for(1) == "http://localhost?s=askdljf&p=1"
    assert paginator.url_for(2) == "http://localhost?s=askdljf&p=2"


def test_paginator_adds_class_to_active_page():
    query = mock.Mock()
    query.count = mock.Mock(return_value=500)
    paginator = Paginator(query, 5, "http://localhost")
    assert 'class="active"' not in paginator.get_page_html(4)
    assert 'class="active"' in paginator.get_page_html(5)
    assert 'class="active"' not in paginator.get_page_html(6)


def test_paginator_dict():
    query = mock.Mock()
    query.count = mock.Mock(return_value=500)
    paginator = Paginator(query, 5, "http://localhost?p=5")
    d = paginator.render_dict()
    assert d["current_page"] == 5
    assert d["total_count"] == 500
    assert d["per_page"] == 50
    assert d["total_pages"] == 10
    assert d["links"]["self"] == "http://localhost?p=5"
    assert d["links"]["next"] == "http://localhost?p=6"
    assert d["links"]["prev"] == "http://localhost?p=4"
    assert d["links"]["first"] == "http://localhost?p=1"
    assert d["links"]["last"] == "http://localhost?p=10"


def test_paginator_dict_first_page():
    query = mock.Mock()
    query.count = mock.Mock(return_value=500)
    paginator = Paginator(query, 1, "http://localhost?p=5")
    d = paginator.render_dict()
    assert d["current_page"] == 1
    assert d["links"]["self"] == "http://localhost?p=1"
    assert d["links"]["next"] == "http://localhost?p=2"
    assert d["links"]["prev"] == None


def test_paginator_dict_last_page():
    query = mock.Mock()
    query.count = mock.Mock(return_value=500)
    paginator = Paginator(query, 10, "http://localhost?p=10")
    d = paginator.render_dict()
    assert d["current_page"] == 10
    assert d["links"]["self"] == "http://localhost?p=10"
    assert d["links"]["next"] == None
    assert d["links"]["prev"] == "http://localhost?p=9"


def test_paginator_dict_only_one_page():
    query = mock.Mock()
    query.count = mock.Mock(return_value=1)
    paginator = Paginator(query, 1, "http://localhost?p=1")
    d = paginator.render_dict()
    assert d["links"]["next"] == None
    assert d["links"]["prev"] == None


def test_paginator_html():
    query = mock.Mock()
    query.count = mock.Mock(return_value=500)
    paginator = Paginator(query, 5, "http://localhost?p=5")
    html = paginator.render_html()
    assert "Showing #201-250 out of 500" in html
    assert '<a href="http://localhost?p=4">4</a>' in html
    assert '<a href="http://localhost?p=5" class="active">5</a>' in html
    assert '<a href="http://localhost?p=6">6</a>' in html
