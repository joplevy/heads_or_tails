jQuery.noConflict();

var heads_tails;

(function($) {
    heads_tails = {
        foundation: {
            init: function() {
                'use strict';
                //Init foundation
                $(document).foundation();
            }
        }
    };

    $(document).ready(function() {
        'use strict';
        heads_tails.foundation.init();
    });

    /*$(window).on('load', function() {
        'use strict';
    });*/
})(jQuery);