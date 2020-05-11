<%@page import="java.text.DecimalFormat"%>
<%@page import="java.sql.*"%>
<%@page import="java.util.*"%>
<%@page import="org.json.JSONObject"%>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>WA3i</title>
</head>
<body>
<%
    request.setCharacterEncoding("utf-8");
    String ques_ans = request.getParameter("ques_ans");
    Connection con = null;
    int n=0;

    Class.forName("com.mysql.jdbc.Driver");
    String DB_URL="jdbc:mysql://localhost:3306/wa3i?useUnicode=true&characterEncoding=utf9";
    con = DriverManager.getConnection(DB_URL,"root", "mysql21!");
    String query = "insert into solve(response) values(?);
    PreparedStatement pstmt = con.prepareStatement(query);

    pstmt.setString(1,response);
    n=pstmt.executeUpdate();
    pstmt.close()

 } catch (Exception e) {
        e.printStackTrace();
    } finally {
        if (con != null) {
            try {
                con.close();
            } catch (Exception e) {
                e.printStackTrace();
                }
        }
    }

%>
<script type="text/javascript">
    if(<%=n%> > 0){
 alert("success...");
    }else {
 alert("fail ...");
    }
    finally{

</script>
</body>
</html>