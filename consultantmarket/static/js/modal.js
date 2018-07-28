$( document ).ready(function() {
  $('#theModal').on('show.bs.modal', function (e) {

    var button = $(e.relatedTarget);
    var modal = $(this);
  
    modal.find('.modal-body').load(button.data("remote"));
  
  });
});