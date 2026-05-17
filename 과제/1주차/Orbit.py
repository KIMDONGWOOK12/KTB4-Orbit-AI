import os
import sys
import random
import asyncio

def wrong_note(quiz, answer):
	with open("wrong.md", "a", encoding="utf-8") as f:
		f.write(f"{quiz} | {answer}\n")
	print("오답 노트가 wrong.md에 자동 기록 되었습니다.")

async def run_quiz():
	if not os.path.exists("note.md"):
		print("note.md에 파일이 없습니다. 파일을 먼저 만들어주세요")
		return

	with open("note.md", "r", encoding="utf-8") as f:
		lines = [line.strip() for line in f.readlines() if "|" in line]

	if not lines:
		print("note.md에 등록된 문제가 없습니다")
		return

	selected_quizzes = random.sample(lines, min(3, len(lines)))
	print(f"총 {len(selected_quizzes)}문제를 출제합니다. 제한시간 10초 입니다.")

	for idx, item in enumerate(selected_quizzes, 1):
		quiz, answer = item.split("|")
		quiz = quiz.strip()
		answer = answer.strip()
		
		print(f"\n[문제{idx}] {quiz}")

		try:
			#비동기
			quiz_input = asyncio.to_thread(input, ">>> 답: ")
			user_answer = await asyncio.wait_for(quiz_input, timeout=10)

			if user_answer.strip() == answer:
				print("정답입니다")
			else:
				print(f"떙 정답은 {answer}입니다!")
				wrong_note(quiz, answer) # 오답노트 저장 함수 호출

		except asyncio.TimeoutError:
			print(f"시간 초과 정답은 {answer}입니다")
			wrong_note(quiz, answer) # 시간 초과도 틀린거

#오답노트 출력 기능( 터미널에 보여주기 )
def show_wrong_note():
	if not os.path.exists("wrong.md") or os.path.getsize("wrong.md") == 0:
		print("\n 오답노트가 비어있습니다. 100점이시거나 틀린 문제가 아직 없습니다.")
		return

	print("\n==================================")
	print("============ 오답 노트 ===========")
	print("\n==================================")
	
	with open("wrong.md", "r", encoding="utf-8") as f:
		lines = f.readlines()
		for idx, line in enumerate(lines, 1):
			if "|" in line:
				quiz, answer = line.strip().split("|")
				print(f"\n[오답 {idx}] {quiz}")
				print(f"[정답] {answer}")
				print("-" * 50) #구분선

#메인 제어 CLI 명령어 분기 처리
def main():
	if len(sys.argv) < 2:
		print("사용법 : python Orbit.py [--quiz / --wrong]")
		return

	command = sys.argv[1]

	if command == "--quiz":
		asyncio.run(run_quiz())


	elif command == "--wrong":
		show_wrong_note()

	else:
		print("알 수 없는 명령어 입니다.")
		print("사용법 : python Orbit.py [--quiz / --wrong]")

if __name__ == "__main__":
	main()