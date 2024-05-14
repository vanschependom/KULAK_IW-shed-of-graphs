var filters = [];
var filterId = 0;

filterCheck = (toCheck) => {
	if (toCheck.value == "only_degree") {
		document.getElementById("amount").style.display = "none";
		document.getElementById("degree").attributes.push("required");
	} else {
		document.getElementById("amount").style.display = "block";
		if (document.getElementById("degree").attributes.required) {
			document.getElementById("degree").attributes.pop("required");
		}
	}
};

handleForm = (e) => {
	e.preventDefault();

	// Show filter container
	if (document.getElementById("filter-container").style.display === "none") {
		document.getElementById("filter-container").style.display = "block";
	}

	// Get values from form
	const form = document.getElementById("filterForm");
	const select = form.elements["filter-type"];
	const filterType = select.options[select.selectedIndex].value;
	var degree = form.elements["degree"].value;

	// convert degree to integer or to list of integers
	if (degree.includes(",")) {
		degree = degree.split(",").map(Number);
	} else {
		degree = parseInt(degree);
	}

	// If filter type is only_degree, amount is not needed
	if (filterType != "only_degree") {
		// convert amount to integer or to list of integers
		var amount = form.elements["amount"].value;
		if (amount.includes(",")) {
			amount = amount.split(",").map(Number);
		} else {
			amount = parseInt(amount);
		}
	}

	var filterObj;

	if (filterType === "only_degree") {
		filterObj = {
			type: filterType,
			degree: degree,
		};
	} else {
		filterObj = {
			type: filterType,
			degree: degree,
			amount: amount,
		};
	}

	var filterList = document.getElementById("filter-list");
	var filterItem = document.createElement("li");
	filterItem.id = filterId;

	if (filterType === "only_degree") {
		filterItem.innerHTML = `${filterType}: Degree ${degree} `;
	} else {
		filterItem.innerHTML = `${filterType}: Degree ${degree}, Amount ${amount} `;
	}

	filterList.appendChild(filterItem);

	console.log(document.getElementById("filter-container").style);

	// make the filter visible
	if (document.getElementById("filter-container").style.display == "") {
		document.getElementById("filter-container").style.display = "block";
	}

	// Clear input fields
	form.reset();

	// Update JSON data
	addFilterToJson(filterType, degree, amount);
};

window.onload = function () {
	document
		.getElementById("filterForm")
		.addEventListener("submit", handleForm);
	console.log("Script loaded");

	document
		.getElementById("clear-filters")
		.addEventListener("click", clearFilters);
};

addFilterToJson = (filterType, degree, amount) => {
	// add filter to filters JSON
	var filterObj = {};
	if (filterType === "only_degree") {
		filterObj[filterType] = {
			degree: degree,
		};
	} else {
		filterObj[filterType] = {
			degree: degree,
			amount: amount,
		};
	}
	filters.push(filterObj);
	// update the hidden input field
	document.getElementById("filters").value = parseJsonString();
	if (document.getElementById("generateButton").style.display === "") {
		document.getElementById("generateButton").style.display = "block";
		document.getElementById("order").style.display = "block";
	}
};

parseJsonString = () => {
	// join all objects in the list
	newFilters = filters.map(JSON.stringify).join(",");
	// remove the curly braces from signle objects
	newFilters = newFilters.replace("},{", ",");
	return newFilters;
};

clearFilters = () => {
	// clear the filters
	filters = [];
	// update the hidden input field
	document.getElementById("filters").value = "";
	// clear the filter list
	document.getElementById("filter-list").innerHTML = "";
	document.getElementById("filter-container").style.display = "none";
	document.getElementById("generateButton").style.display = "none";
	document.getElementById("order").style.display = "none";
};
