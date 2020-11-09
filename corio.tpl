<html>
 <head>
  <title>Results</title>
  <script>
  function goBack() {
     window.history.back()
  }
  </script>
 </head>
 <body>
  <h1>Results for {{address}}</h1>
  <div>
   {{serial}}
  </div>
  %for item in serialcard:
   <div>{{item}}</div>
  %end
  <div>
   <button onclick="goBack()">Go Back</button>
  </div>
 </body>
</html>
