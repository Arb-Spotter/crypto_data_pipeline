CREATE VIEW tokens_market_data AS
SELECT tokens.name, tokens.thumb, tokens.large, market_data.*
FROM tokens
JOIN market_data ON tokens.token = market_data.token
ORDER BY tokens.token;