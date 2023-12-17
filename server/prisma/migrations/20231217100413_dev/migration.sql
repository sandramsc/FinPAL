-- DropForeignKey
ALTER TABLE "User" DROP CONSTRAINT "User_telegramThreadId_fkey";

-- AlterTable
ALTER TABLE "User" ALTER COLUMN "telegramThreadId" DROP NOT NULL;

-- AddForeignKey
ALTER TABLE "User" ADD CONSTRAINT "User_telegramThreadId_fkey" FOREIGN KEY ("telegramThreadId") REFERENCES "Thread"("id") ON DELETE SET NULL ON UPDATE CASCADE;
