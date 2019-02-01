(($) => {

    'use strict';

    let $controls = $("#controls");

    $controls.find('input,select').on('change', () => {
         $controls.submit();
    });

})(jQuery);