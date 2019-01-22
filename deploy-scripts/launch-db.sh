aws dynamodb create-table \
    --table-name RentalatedAccounts \
    --attribute-definitions \
        AttributeName=Email, AttributeType=S \
    --key-schema AttributeName=Email, KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1

