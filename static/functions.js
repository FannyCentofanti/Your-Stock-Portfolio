{
    $(document).ready(function()
    {
        if (location.pathname == '/buy' || location.pathname == '/sell')
        {
            if (/[?&]symbol=/.test(location.search))
            {
                var searchParams = new URLSearchParams(window.location.search);
                var symbol = searchParams.get('symbol');
                $('#symbol_input').val(symbol);
            }
            else
            {
                console.log("Missing querystring parameter");
            }
        }
    });

    function indexBuy(symbol)
    {
        if (symbol != null)
        {
            window.location.href = '/buy?symbol=' + symbol;
        }
        else
        {
            window.location.href = '/buy'
        }
    }

    function indexSell(symbol)
    {
        if (symbol != null)
        {
            window.location.href = '/sell?symbol=' + symbol;
        }
        else
        {
            window.location.href = '/sell'
        }
    }

}