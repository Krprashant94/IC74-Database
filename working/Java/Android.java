import java.sql.*;
import java.util.*;

public class Android {
	public static void main( String args[] ) {

		Connection c = null;
		Statement stmt = null;
		try {
			Class.forName("org.sqlite.JDBC");
			c = DriverManager.getConnection("jdbc:sqlite:74XX.db");
			c.setAutoCommit(false);
			stmt = c.createStatement();
			ResultSet rs = stmt.executeQuery( "SELECT * FROM IC74SERIES;" );
			ArrayList tmp = new ArrayList();
			ArrayList<ArrayList> result = new ArrayList<ArrayList>();
			while ( rs.next() ) {
				tmp = new ArrayList();
				tmp.add(rs.getString("IC_NO"));
				tmp.add(rs.getString("UNIT"));
				tmp.add(rs.getString("PINS"));
				tmp.add(rs.getString("DISC"));
				tmp.add(rs.getString("DIMENSION"));
				tmp.add(rs.getString("INPUT"));
				tmp.add(rs.getString("OUTPUT"));
				tmp.add(rs.getString("TYPE"));
				tmp.add(rs.getString("PACKAGE"));
				result.add(tmp);
			}
			rs.close();
			stmt.close();
			c.close();
			for (int i=0; i<result.size(); i++) 
			{
				for(int j=0; j<result.get(i).size(); j++){
					System.out.println(result.get(i).get(j));
				}
			}
		} catch ( Exception e ) {
			System.err.println( e.getClass().getName() + ": " + e.getMessage() );
			System.exit(0);
		}
	}
}