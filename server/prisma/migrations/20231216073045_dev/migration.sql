/*
  Warnings:

  - You are about to drop the column `type` on the `Thread` table. All the data in the column will be lost.
  - Added the required column `platform` to the `Thread` table without a default value. This is not possible if the table is not empty.

*/
-- CreateEnum
CREATE TYPE "ThreadPlatform" AS ENUM ('telegram');

-- AlterTable
ALTER TABLE "Thread" DROP COLUMN "type",
ADD COLUMN     "platform" "ThreadPlatform" NOT NULL;

-- DropEnum
DROP TYPE "ThreadType";
