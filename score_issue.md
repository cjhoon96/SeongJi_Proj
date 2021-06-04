### 스코어가 이상하게 출력되던 문제

blit_score(score)만 수정함  

결론적으로 점수를 출력하는 함수로 새로 만들었음.

기존의 문제점은 n_score는 while문 마다 갱신되지만

점수 폰트는 동작마다 갱신된다는 것이었음.

갱신 주기를 통일하기 위해 n_score 변수 지정과 screen.blit()을 묶은 blit_score() 함수를 만들고,

유저 동작 시마다 blit_score()를 호출함.