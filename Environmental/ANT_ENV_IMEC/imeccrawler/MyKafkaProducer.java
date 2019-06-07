/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package imeccrawler;

import java.util.Properties;
import java.util.ArrayList;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.producer.RecordMetadata;


/**
 *
 * @author gilman
 */
public class MyKafkaProducer {
    
    //basic for local testing purposes, modify as needed
    
    public KafkaProducer producer;
    private boolean to_use;
    
    public MyKafkaProducer(boolean to_use){
    
        Properties kafkaProps = new Properties(); 
        kafkaProps.put("bootstrap.servers", "localhost:9092");
        kafkaProps.put("key.serializer","org.apache.kafka.common.serialization.StringSerializer"); 
        kafkaProps.put("value.serializer","org.apache.kafka.common.serialization.StringSerializer");

        producer = new KafkaProducer<String, String>(kafkaProps); 
    }
    
    public void sendMessage(ProducerRecord<String, String> record){
        try {
            if(to_use){
                RecordMetadata rm = (RecordMetadata)producer.send(record).get();
                System.out.println("Offset:"+String.valueOf(rm.offset()));
            }
        } catch (Exception e) {
            e.printStackTrace(); 
        }
    }
    
    public void sendMessagesForTopic(String topic, ArrayList<String> values){
       try {
           if(to_use){
            for(String value:values){
                ProducerRecord<String, String> record = new ProducerRecord(topic,value);
                RecordMetadata rm = (RecordMetadata)producer.send(record).get();
                System.out.println("Offset:"+String.valueOf(rm.offset()));
            }
           }
        } catch (Exception e) {
            e.printStackTrace(); 
        } 
    }
    
}
