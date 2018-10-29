window.sr = ScrollReveal();

var reveal3000 = {
	duration: 3000,
	mobile: false
}

var revealBottom = {
	duration: 1000,
	origin: 'bottom',
	distance: '100px',
	viewFactor: 0,
	mobile: false
};

var revealBottomScale = {
	duration: 1000,
	origin: 'bottom',
	distance: '100px',
	scale: 0.5,
	viewFactor: 0,
	mobile: false
};

var revealTop = {
	duration: 1000,
	origin: 'top',
	distance: '100px',	
	viewFactor: 0,
	mobile: false
};

var revealLeft = {
	duration: 1000,
	origin: 'left',
	distance: '300px',
	viewFactor: 0,
	mobile: false
};

var revealRight = {
	duration: 1000,
	origin: 'right',
	distance: '300px',
	viewFactor: 0,
	mobile: false
};

sr.reveal('.reveal-3000', reveal3000);
sr.reveal('.reveal-top', revealTop);
sr.reveal('.reveal-bottom', revealBottom);
sr.reveal('.reveal-bottom-fast', revealBottom);
sr.reveal('.reveal-bottom-scale', revealBottomScale);
sr.reveal('.reveal-left', revealLeft);
sr.reveal('.reveal-right', revealRight);