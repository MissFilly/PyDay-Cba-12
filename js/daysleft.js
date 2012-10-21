var today = new Date();
var pyday = new Date(2012, 8, 15);
var day = 24*60*60*1000;
var daysLeft = Math.ceil((pyday.getTime() - today.getTime())/day);
var wordLeft = "Faltan ";
var wordDay = " días";

if (daysLeft == 1) {
	wordDay = " día";
	wordLeft = "Falta ";
}
else if (daysLeft < 0) {
	daysLeft = 0;
}

document.write(wordLeft + "<span>" + daysLeft + "</span>" + wordDay);