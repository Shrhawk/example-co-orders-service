serverless-offline:
	serverless offline \
			--host 0.0.0.0 \
			--httpPort 8080 \
			--lambdaPort 3000 \
			--region us-east-1 \

test:
	pytest;

test-style:
	py.test