$(document).ready(function () {
    $('#titulo_filme').on('input', function () {
        var inputText = $(this).val();

        $.ajax({
            type: 'GET',
            url: '/get_sugestoes',
            data: {'inputText': inputText},
            success: function (sugestoes) {
                var dropdown = $('#sugestoes');
                dropdown.empty();

                if (sugestoes.length > 0) {
                    dropdown.append('<option value="Opções">Opções</option>');

                    for (var i = 0; i < sugestoes.length; i++) {
                        dropdown.append('<option value="' + sugestoes[i] + '">' + sugestoes[i] + '</option>');
                    }
                    dropdown.show();
                } else {
                    dropdown.hide();
                }
            }
        });
   });

    $('#sugestoes').on('change', function () {
        var selectedSugestao = $(this).val();
        $('#titulo_filme').val(selectedSugestao);
        $(this).hide();
    });
});
