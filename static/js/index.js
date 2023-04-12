// 定义一个数组，保存当前所有页面的class name
function get_page_index() {
	var page_index = [];
	var divs = document.getElementsByClassName("div");
	for (var i = 0; i < divs.length; i++) {
		if (divs[i].className.indexOf("page__") != -1) {
			page_index.push(divs[i].className);
		}
	};
	return page_index;
}

// //默认将第一页显示出来
// window.onload = function () {
// 	var page_index = get_page_index();
// 	page_option(page_index[0]);
// }

// 输入index，打开指定的div，隐藏其他的div
function page_option(index) {
	var page_index = get_page_index();
	if (index.indexOf("page__") != -1) {
		var div = 0;
	}
	else {
		index = "page__" + index;
	}
	for (var i = 0; i < page_index.length; i++) {
		if (page_index[i] != index) {
			page_index[i].style.display = "none";
		}
		else {
			page_index[i].style = "padding: 30px;padding-top: 0px;padding-bottom: 0px;";
		}
	}

};

// 点击 返回第一页按钮 执行的操作
function first_click() {
	var page_index = get_page_index();
	page_option(0);
	document.getElementById('currentPage').value = 1;

}

// 点击 跳到最后一页按钮 执行的操作
function last_click() {
	var page_index = get_page_index();

	var total_page = document.getElementById('totalPage').value;
	page_option(page_index[page_index.length - 1]);
	document.getElementById('currentPage').value = total_page;
}


// 点击 上一页按钮 执行的操作
function prev_click() {
	var cur_page = document.getElementById('currentPage').value;
	if (cur_page > 1) {
		document.getElementById('currentPage').value = parseInt(cur_page) - 1;
		var pagename = page_index[parseInt(cur_page) - 2];
		page_option(pagename);
	}
}

// 点击 下一页按钮 执行的操作
function next_click() {

	var page_index = get_page_index();

	var cur_page = parseInt(document.getElementById('currentPage').value);
	var total_page = int(page_index.length) //document.getElementById('totalPage').value;
	if (cur_page < total_page) {
		document.getElementById('currentPage').value = parseInt(cur_page) + 1;
		var pagename = page_index[parseInt(cur_page) + 1];
		page_option(pagename);
	}

}

// 手动改变当前页码时执行的操作
function choose_page() {

	var page_index = get_page_index();

	var cur_page = document.getElementById('currentPage').value;
	var pagename = page_index[parseInt(cur_page) - 1];
	page_option(pagename);
}
