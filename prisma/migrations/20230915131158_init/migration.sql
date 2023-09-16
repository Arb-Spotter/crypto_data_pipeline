-- CreateTable
CREATE TABLE "tokens" (
    "token" TEXT NOT NULL
);

-- CreateTable
CREATE TABLE "exchanges" (
    "exchange" TEXT NOT NULL
);

-- CreateTable
CREATE TABLE "one_min_ohlcv_data" (
    "token" TEXT NOT NULL,
    "open" DOUBLE PRECISION NOT NULL,
    "high" DOUBLE PRECISION NOT NULL,
    "low" DOUBLE PRECISION NOT NULL,
    "close" DOUBLE PRECISION NOT NULL,
    "volume" DOUBLE PRECISION NOT NULL,
    "exchange" TEXT NOT NULL,
    "updatedAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "one_min_ohlcv_data_pkey" PRIMARY KEY ("token","updatedAt","exchange")
);

-- CreateTable
CREATE TABLE "one_hour_ohlcv_data" (
    "token" TEXT NOT NULL,
    "open" DOUBLE PRECISION NOT NULL,
    "high" DOUBLE PRECISION NOT NULL,
    "low" DOUBLE PRECISION NOT NULL,
    "close" DOUBLE PRECISION NOT NULL,
    "volume" DOUBLE PRECISION NOT NULL,
    "exchange" TEXT NOT NULL,
    "updatedAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "one_hour_ohlcv_data_pkey" PRIMARY KEY ("token","updatedAt","exchange")
);

-- CreateTable
CREATE TABLE "one_day_ohlcv_data" (
    "token" TEXT NOT NULL,
    "open" DOUBLE PRECISION NOT NULL,
    "high" DOUBLE PRECISION NOT NULL,
    "low" DOUBLE PRECISION NOT NULL,
    "close" DOUBLE PRECISION NOT NULL,
    "volume" DOUBLE PRECISION NOT NULL,
    "exchange" TEXT NOT NULL,
    "updatedAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "one_day_ohlcv_data_pkey" PRIMARY KEY ("token","updatedAt","exchange")
);

-- CreateIndex
CREATE UNIQUE INDEX "tokens_token_key" ON "tokens"("token");

-- CreateIndex
CREATE UNIQUE INDEX "exchanges_exchange_key" ON "exchanges"("exchange");

-- AddForeignKey
ALTER TABLE "one_min_ohlcv_data" ADD CONSTRAINT "one_min_ohlcv_data_token_fkey" FOREIGN KEY ("token") REFERENCES "tokens"("token") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "one_hour_ohlcv_data" ADD CONSTRAINT "one_hour_ohlcv_data_token_fkey" FOREIGN KEY ("token") REFERENCES "tokens"("token") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "one_day_ohlcv_data" ADD CONSTRAINT "one_day_ohlcv_data_token_fkey" FOREIGN KEY ("token") REFERENCES "tokens"("token") ON DELETE RESTRICT ON UPDATE CASCADE;
