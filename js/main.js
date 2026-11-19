/*
	Spatial by TEMPLATED
	templated.co @templatedco
	Released for free under the Creative Commons Attribution 3.0 license (templated.co/license)
*/

(function($) {

	skel.breakpoints({
		xlarge:	'(max-width: 1680px)',
		large:	'(max-width: 1280px)',
		medium:	'(max-width: 980px)',
		small:	'(max-width: 736px)',
		xsmall:	'(max-width: 480px)'
	});

	$(function() {

		var	$window = $(window),
			$body = $('body');

		// Disable animations/transitions until the page has loaded.
			$body.addClass('is-loading');

			function pageLoaded() {
				window.setTimeout(function() {
					$body.removeClass('is-loading');
				}, 100);
			}

			// jQuery 3 runs ready handlers asynchronously, so "load" may already have fired.
			if (document.readyState === 'complete')
				pageLoaded();
			else
				$window.on('load', pageLoaded);

		// Fix: Placeholder polyfill.
			$('form').placeholder();

		// Prioritize "important" elements on medium.
			skel.on('+medium -medium', function() {
				$.prioritize(
					'.important\\28 medium\\29',
					skel.breakpoint('medium').active
				);
			});

		// Off-Canvas Navigation.

			// Title Bar (only visible on medium and below, where #header is hidden).
				$(
					'<div id="titleBar">' +
						'<a href="#navPanel" class="toggle" aria-label="Open menu"></a>' +
						'<a href="/" class="title">Tobias Hinz</a>' +
					'</div>'
				)
					.appendTo($body);

			// Navigation Panel (nav links + social icons from #header).
				$(
					'<div id="navPanel" aria-label="Menu">' +
						'<nav>' + $('#nav').html() + '</nav>' +
						'<ul class="icons">' + $('#header ul.icons').html() + '</ul>' +
						'<a href="#navPanel" class="close" aria-label="Close menu"></a>' +
					'</div>'
				)
					.appendTo($body)
					.panel({
						delay: 500,
						hideOnClick: true,
						hideOnSwipe: true,
						resetScroll: true,
						resetForms: true,
						side: 'left'
					});

			// Fix: Remove transitions on WP<10 (poor/buggy performance).
				if (skel.vars.os == 'wp' && skel.vars.osVersion < 10)
					$('#navPanel')
						.css('transition', 'none');


	});

})(jQuery);