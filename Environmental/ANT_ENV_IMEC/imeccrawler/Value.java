/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package imeccrawler;
import ch.hsr.geohash.GeoHash;

/**
 *
 * @author gilman
 */
public class Value {
    public Long time;
    public String geohash;
    public String sourceId;
    public float value;
    
    public Value(Long time, String geohash, String sourceId, float value){
        this.time = time;
        this.geohash=geohash;
        this.sourceId=sourceId;
        this.value=value;
    }
    
    @Override
    public String toString(){
        return "time="+time+" geohash="+geohash+" sourceId="+sourceId+" value="+value;
    }
    
    public String toCSV(){
        return time+","+geohash+","+sourceId+","+value;
    }
    
    public String toCSVCoordinates(){
       GeoHash geo = GeoHash.fromGeohashString(geohash);
       return time+","+geohash+","+geo.getPoint().getLatitude()+","+geo.getPoint().getLongitude()+","+sourceId+","+value;
    }
    
     public String toJSONCoordinates(){
       GeoHash geo = GeoHash.fromGeohashString(geohash);
       return "{\"timestamp\":"+time+",\"geohash\":"+geohash+",\"latitude\":"+geo.getPoint().getLatitude()+",\"longitude\":"+geo.getPoint().getLongitude()+",\"sourceId\":"+sourceId+",\"value\":"+value+"}";
    }
    
    public String toString(String output_format){
        if(output_format.equalsIgnoreCase("JSON"))
            return toJSONCoordinates();
        else if (output_format.equalsIgnoreCase("CSV"))
            return toCSVCoordinates();
        else {
            System.out.println("FileWritler: check output_format string in prop file, only JSON and CSV are available.");
            return "";
        }
    }
}
