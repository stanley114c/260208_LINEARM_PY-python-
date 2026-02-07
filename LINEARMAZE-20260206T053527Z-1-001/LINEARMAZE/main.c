#include <stdio.h>
#include <string.h>

#define N 25
#define MAXQ (N * N)

typedef struct { int r, c; } Point;

// 更新為 25x25 地圖
int maze[25][25] = {
 {1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1},
 {1,1,1,1,0,1,1,1,1,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,1},
 {1,0,0,0,0,0,0,1,1,0,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1},
 {1,1,1,1,1,1,0,1,1,0,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1},
 {1,1,1,1,1,1,0,1,1,0,1,1,1,1,0,1,1,0,1,1,1,1,0,1,1},
 {1,1,0,0,0,0,0,1,1,0,1,1,1,1,0,1,1,0,0,0,0,1,0,1,1},
 {1,1,1,1,1,1,0,1,1,0,0,0,0,0,0,1,1,1,1,1,1,1,0,1,1},
 {1,1,1,1,1,1,0,1,1,1,1,0,1,1,0,1,1,1,1,0,0,0,0,1,1},
 {1,1,0,0,0,0,0,1,1,1,1,0,1,1,0,0,0,1,1,0,0,1,1,1,1},
 {1,1,1,0,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,1,1,1,1},
 {1,1,1,0,1,1,0,0,0,0,0,0,1,1,1,1,0,1,1,1,1,1,1,1,1},
 {1,0,0,0,1,1,1,1,1,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,1},
 {1,0,1,0,0,0,1,1,1,1,1,0,1,1,1,1,0,1,1,0,1,1,1,1,1},
 {1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1},
 {1,0,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1},
 {1,0,1,0,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,0,1,1},
 {1,0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,0,0,0,0,0,1},
 {1,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,0,1,1,0,1,1,1,1,1},
 {1,1,0,1,1,0,1,1,1,1,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0},
 {1,1,0,1,1,0,1,1,1,1,0,0,0,0,1,1,0,1,1,0,1,1,0,1,1},
 {1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,0,1,1,0,1,1},
 {1,1,0,1,1,1,0,0,0,0,0,0,0,0,1,1,0,1,1,0,1,1,0,1,1},
 {1,1,0,1,1,1,1,1,1,0,1,1,1,0,1,1,0,1,1,0,1,1,1,1,1},
 {1,1,1,1,0,0,0,0,0,0,1,1,1,0,1,1,0,0,0,0,0,0,1,1,1},
 {1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1}
};


int dist[N][N];
Point path[MAXQ];
int path_len = 0;

void flood_fill(Point start) {
    for (int r = 0; r < N; r++) for (int c = 0; c < N; c++) dist[r][c] = -1;
    Point q[MAXQ];
    int head = 0, tail = 0;
    dist[start.r][start.c] = 0;
    q[tail++] = start;
    int dr[] = {-1, 1, 0, 0}, dc[] = {0, 0, -1, 1};
    while (head < tail) {
        Point cur = q[head++];
        for (int k = 0; k < 4; k++) {
            int nr = cur.r + dr[k], nc = cur.c + dc[k];
            if (nr>=0 && nr<N && nc>=0 && nc<N && maze[nr][nc]==0 && dist[nr][nc]==-1) {
                dist[nr][nc] = dist[cur.r][cur.c] + 1;
                q[tail++] = (Point){nr, nc};
            }
        }
    }
}

void backtrace_path(Point start, Point end) {
    if (dist[end.r][end.c] == -1) {
        printf("警告：終點不可達！\n");
        return;
    }
    Point cur = end;
    while (!(cur.r == start.r && cur.c == start.c)) {
        path[path_len++] = cur;
        int dr[] = {-1, 1, 0, 0}, dc[] = {0, 0, -1, 1};
        for (int k = 0; k < 4; k++) {
            int nr = cur.r + dr[k], nc = cur.c + dc[k];
            if (nr>=0 && nr<N && nc>=0 && nc<N && dist[nr][nc] == dist[cur.r][cur.c]-1) {
                cur = (Point){nr, nc};
                break;
            }
        }
    }
    path[path_len++] = start;
}

void export_for_python(const char* filename) {
    FILE *fp = fopen(filename, "w");
    if (!fp) return;
    fprintf(fp, "%d\n", N);
    for (int r = 0; r < N; r++) {
        for (int c = 0; c < N; c++) fprintf(fp, "%d ", maze[r][c]);
        fprintf(fp, "\n");
    }
    fprintf(fp, "%d\n", path_len);
    for (int i = path_len - 1; i >= 0; i--) {
        fprintf(fp, "%d %d\n", path[i].r, path[i].c);
    }
    fclose(fp);
}

int main() {
    // 根據截圖：起點在最下方出口 (Row 24, Column 13)
    Point start = {24, 13};

    // 終點在上方紅色 4x4 區塊的起始點 (Row 5, Column 19)
    // 注意：BFS 只需要走到該區塊的其中一格即可
    Point end = {7, 19};

    flood_fill(start);
    backtrace_path(start, end);

    export_for_python("animation");

    if (path_len > 0) {
        printf("路徑生成成功！總長度：%d 步。\n", path_len);
    } else {
        printf("警告：找不到路徑，請檢查座標是否落在牆壁上。\n");
    }

    return 0;
}
