// save class name
function get_page_index() {
	var page_index = [];
	var divs = document.getElementsByClassName("seal_picture");
	for (var i = 0; i < divs.length; i++) {
		page_index.push(divs[i].id);
	};
	return page_index;
}


// Open the specified div
function page_option(index) {
	var divs = document.getElementsByClassName("seal_picture");
	for (var i = 0; i < divs.length; i++) {
		divs[i].style = "display: none;";
	}
	divs[index].style = "padding: 30px;padding-top: 0px;padding-bottom: 0px;";
};

// Back to the first page button
function first_click() {
	var page_index = get_page_index();
	page_option(0);
	document.getElementById('currentPage').value = 1;

}

// Back to the last page button
function last_click() {
	var page_index = get_page_index();

	var total_page = document.getElementById('totalPage').value;
	page_option(page_index[page_index.length - 1]);
	document.getElementById('currentPage').value = total_page;
}

// previous page button
function prev_click() {
	var page_index = get_page_index();
	var cur_page = document.getElementById('currentPage').value;
	if (cur_page > 1) {
		document.getElementById('currentPage').value = parseInt(cur_page) - 1;
		var pagename = page_index[parseInt(cur_page) - 2];
		page_option(pagename);
	}
}

// next page button
function next_click() {

	var page_index = get_page_index();

	var cur_page = parseInt(document.getElementById('currentPage').value);
	var total_page = document.getElementById('totalPage').value;
	if (cur_page < total_page) {
		document.getElementById('currentPage').value = parseInt(cur_page) + 1;
		var pagename = page_index[parseInt(cur_page) + 1];
		page_option(pagename);
	}

}

// Jump to the specified page
function choose_page() {

	var page_index = get_page_index();

	var cur_page = document.getElementById('currentPage').value;
	var pagename = page_index[parseInt(cur_page) - 1];
	page_option(pagename);
}
