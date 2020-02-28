declare -a KafkaTopics=("ANTA_ENV_WEATHERFORECAST_DAILY" 
                        "CORK_ENV_WATERQUALITY_YEARLY"
                        "CORK_ENV_WEATHERFORECAST_DAILY"
                        "THESS_ENV_WATERQUALITY_CHLOR_YEARLY"
                        "THESS_ENV_WATERQUALITY_NUTRIENTS_YEARLY"
                        "THESS_ENV_WATERQUALITY_YEARLY"
                        "THESS_ENV_WEATHERFORECAST_DAILY")
 
# Read the array values with space
for val in "${KafkaTopics[@]}"; do
  kafka-topics.sh --bootstrap-server ${KAFKA_HOST}:${KAFKA_PORT} --create --topic ${val} --partitions 3 --replication-factor 2
  echo "Topic $val has been created with 3 partitions and replication factor 2 !"
  sleep 5s
done