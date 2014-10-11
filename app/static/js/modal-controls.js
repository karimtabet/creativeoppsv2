//Select a random photo for image fader
function randomOwl(owlSelector) {
    owlSelector.children().sort(function(){
        return Math.round(Math.random()) - 0.5;
    }).each(function(){
        $(this).appendTo(owlSelector);
    });
}
//Image fader settings
$(document).ready(function() {
  $("#image_fader").owlCarousel({
    singleItem: true,
    transitionStyle: "fade",
    autoPlay: true,
    pagination: false,
    beforeInit : function(elem){
      randomOwl(elem);
    }
  });
});
//Project image scroller settings
function openModal(project) {
    var projectId = "#" + project;
    $(projectId).modal({
        onOpen: function (dialog) {
            dialog.overlay.fadeIn('medium');
            dialog.data.fadeIn('medium');
            dialog.container.slideDown('medium');
        },
        onClose: function(dialog) {
            dialog.data.fadeOut('medium');
            dialog.container.slideUp('medium');
            dialog.overlay.fadeOut('medium', function () {
                $.modal.close();
            });
        },
        autoResize:true,
        overlayClose:true
    });
    var owlPhoto = $('.modal_photo_carousel');
    owlPhoto.owlCarousel({
        center:true,
        items:4,
        loop:true,
        margin:10,
        autoplay:true,
        autoWidth:true,
        lazyLoad:true,
        dots:false
    });
    return false;
}