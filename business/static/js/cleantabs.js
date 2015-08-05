/* Clean Tabs: responsive tabs to accordion */

/* Version 1.1: Added the possibility to nest tabs. */
/* Works with the following themes: empty, clear, dark, linear, metro1-2-3-4, stock1-2-3, bordy1-2, fullscreen */

(function($) {

	$.fn.cleanTabs = function(options) {

		var base = $(this);

		// Single tab content
        base.$tab_content = base.find(" > .tab-contents > .tab_content");

		// Horizontal navigation
		base.$nav = base.find(" > ul.tab-nav > li");

		// Vertical navigation
		base.$v_nav = base.find(" > .tab-contents > .v_nav");

		// Options
		base.options = $.extend({},$.fn.cleanTabs.defaultOptions, options);




		// Hide all except for first content
		base.$tab_content.not(":first").hide();




		// Horizontal click
		base.$nav.on("click", function() {

			// Hide content
			base.$tab_content.hide();

			// Set a new variable
			var h_active = $(this).attr("data-tab"); 
			$("#"+h_active).fadeIn(base.options.speed);		

			// New active class
			base.$nav.removeClass("active");
			$(this).addClass("active");
			
			// Adjust between horizontal and vertical
			base.$v_nav.removeClass("v_active");
			$(".v_nav[data-tab^='"+h_active+"']").addClass("v_active");
	
		});


		// Vertical click
		base.$v_nav.on("click", function() {

			// Hide content
			base.$tab_content.hide();

			// Set a new variable
			var v_active = $(this).attr("data-tab"); 
			$("#"+v_active).fadeIn(base.options.speed);

			// New active class
			base.$v_nav.removeClass("v_active");
			$(this).addClass("v_active");

			// Adjust between horizontal and vertical
			base.$nav.removeClass("active");
			$("ul.tab-nav li[data-tab^='"+v_active+"']").addClass("active");

		});


	};
	
    $.fn.cleanTabs.defaultOptions = {
        "speed": 300
    };

})(jQuery);