/*
  Warnings:

  - You are about to drop the column `file` on the `Message` table. All the data in the column will be lost.

*/
-- CreateEnum
CREATE TYPE "Category" AS ENUM ('Grocery', 'FoodAndDining', 'RentAndMortgage', 'Utilities', 'Transportation', 'Entertainment', 'Healthcare', 'Clothing', 'Education', 'Miscellaneous');

-- AlterTable
ALTER TABLE "Message" DROP COLUMN "file",
ADD COLUMN     "photo" TEXT;

-- CreateTable
CREATE TABLE "Transaction" (
    "id" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "amountOut" TEXT,
    "amountIn" TEXT,
    "currency" TEXT,
    "from" TEXT,
    "to" TEXT,
    "category" "Category" NOT NULL DEFAULT 'Miscellaneous',
    "description" TEXT,
    "transactionDate" TIMESTAMP(3),

    CONSTRAINT "Transaction_pkey" PRIMARY KEY ("id")
);
