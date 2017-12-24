	$('.scrollTo').on('click', function(e) {
		e.preventDefault();
		var getElem = $(this).attr('href');
		if($(getElem).length) {
			var getOffset = $(getElem).offset().top;
			$('html,body').animate({
				scrollTop: getOffset - 60
			}, 500);
		}
		return false;
	});
