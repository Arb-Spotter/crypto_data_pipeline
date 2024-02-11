-- DropForeignKey
ALTER TABLE "market_data" DROP CONSTRAINT "market_data_token_fkey";

-- DropForeignKey
ALTER TABLE "one_day_ohlcv_data" DROP CONSTRAINT "one_day_ohlcv_data_token_fkey";

-- DropForeignKey
ALTER TABLE "one_hour_ohlcv_data" DROP CONSTRAINT "one_hour_ohlcv_data_token_fkey";

-- DropForeignKey
ALTER TABLE "one_min_ohlcv_data" DROP CONSTRAINT "one_min_ohlcv_data_token_fkey";

-- AddForeignKey
ALTER TABLE "one_min_ohlcv_data" ADD CONSTRAINT "one_min_ohlcv_data_token_fkey" FOREIGN KEY ("token") REFERENCES "tokens"("token") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "one_hour_ohlcv_data" ADD CONSTRAINT "one_hour_ohlcv_data_token_fkey" FOREIGN KEY ("token") REFERENCES "tokens"("token") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "one_day_ohlcv_data" ADD CONSTRAINT "one_day_ohlcv_data_token_fkey" FOREIGN KEY ("token") REFERENCES "tokens"("token") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "market_data" ADD CONSTRAINT "market_data_token_fkey" FOREIGN KEY ("token") REFERENCES "tokens"("token") ON DELETE CASCADE ON UPDATE CASCADE;
