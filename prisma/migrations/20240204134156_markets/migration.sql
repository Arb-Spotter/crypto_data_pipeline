-- CreateTable
CREATE TABLE "market_data" (
    "token" TEXT NOT NULL,
    "open" DOUBLE PRECISION,
    "high" DOUBLE PRECISION,
    "low" DOUBLE PRECISION,
    "close" DOUBLE PRECISION,
    "volume" DOUBLE PRECISION,
    "exchange" TEXT NOT NULL,
    "percentage_change" DOUBLE PRECISION,
    "change" DOUBLE PRECISION,
    "b_a_spread" DOUBLE PRECISION,
    "updatedAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "market_data_pkey" PRIMARY KEY ("token","updatedAt","exchange")
);

-- AddForeignKey
ALTER TABLE "market_data" ADD CONSTRAINT "market_data_token_fkey" FOREIGN KEY ("token") REFERENCES "tokens"("token") ON DELETE RESTRICT ON UPDATE CASCADE;
