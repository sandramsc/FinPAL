/*
  Warnings:

  - You are about to drop the column `threadId` on the `User` table. All the data in the column will be lost.
  - Added the required column `telegramThreadId` to the `User` table without a default value. This is not possible if the table is not empty.

*/
-- DropForeignKey
ALTER TABLE "User" DROP CONSTRAINT "User_threadId_fkey";

-- AlterTable
ALTER TABLE "User" DROP COLUMN "threadId",
ADD COLUMN     "telegramThreadId" TEXT NOT NULL;

-- AddForeignKey
ALTER TABLE "User" ADD CONSTRAINT "User_telegramThreadId_fkey" FOREIGN KEY ("telegramThreadId") REFERENCES "Thread"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
