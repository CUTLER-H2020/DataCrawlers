/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package imeccrawler;

import com.google.gson.Gson;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Base64;
import org.apache.kafka.clients.producer.ProducerRecord;

/**
 *
 * @author gilman
 */
public class ImecCrawler {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // get the properties entry point
        RPTManager prop = RPTManager.getInstance();
        // put here your authorization string!!!
        String authorization_string="";
         try{
            String authString = Base64.getEncoder().encodeToString((authorization_string).getBytes("UTF-8"));
            //initiate connection to imec server
            ServerConnection servcon= ServerConnection.getInstance(prop.certificate);
            //handle token
            Authorization authoriz = Authorization.getInstance(authString);
            String token = authoriz.getToken();
            //metrics to get the data for
            String[] metrics = {"channel.waterlevel", "precipitation", "sewer.waterlevel"};
            
            Gson gson = new Gson();
            //file writing object
            FileWriter fw = new FileWriter(prop.output_format);
            //kafka producer object
            MyKafkaProducer kafka = new MyKafkaProducer(prop.kafka_use);
            
            long till_current_time = System.currentTimeMillis();
            for(String metric:metrics){
                //build request to get the data from the last update till current time
                
                String request = "https://idlab-iot.tengu.io/api/v1/scopes/other.cutler/query/"+metric+"/events?"+"from="+prop.data_last_update+"&to="+till_current_time;
                //System.out.println(metric);
                //send request and handle response
                String serv = servcon.sendGet(request,token);
                //System.out.println(serv);
                MetricValue metricValue = gson.fromJson(serv, MetricValue.class);
                ArrayList<Value> values= metricValue.getValues();
               
                //kafka
                //if kafka is in use, appropriate configuration should be made within MyKafkaProducer class
                //here, all sensors put messages under test topic
                
                for(Value val:values){
                    System.out.println(val.toString());
                    kafka.sendMessage(new ProducerRecord("test",gson.toJson(val)));
                }
                //writing to the files
                HashMap hm = metricValue.getValuesGroupedBySourceID(values);
                hm.forEach((k,v)->fw.writeToFile(metric, String.valueOf(k).replaceAll(":", "_"), (ArrayList) v,prop.data_folders_path));  
            }
            //update last update info in the properties file
            prop.setDataLastUpdate(till_current_time);
            
        }catch (Exception ex){
            ex.printStackTrace();
        }
    }
}
