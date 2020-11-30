function keigenvector(path, k)
    colors = {'#3498db', '#e74c3c', '#1abc9c', '#f39c12', '#95a5a6', '#34495e'};
    E = csvread(path);

    %%%%%% step 1
    col1 = E(:,1);
    col2 = E(:,2);
    max_ids = max(max(col1, col2));
    As = sparse(col1, col2, 1, max_ids, max_ids);
    A = full(As); % NxN

    %%%%%% step 2
    D = diag(sum(A, 2));
    L = D^(-1/2)*A*D^(-1/2);


    %%%%%% step 3
    [X, XD] = eig(L); % NxN
    X = X(:, end-k+1:end);
    % figure;
    % plot(sort(diag(XD(end-9:end, end-9:end)), "descend"));
    % xlabel("Sorted position");
    % ylabel("Eigenvalue");
    % title("Top 10 eigenvalues");
    XD = XD(end-k+1:end, end-k+1:end);
    XD = diag(sort(diag(XD), "descend"));
    disp("Diagonal for X");
    disp(XD);

    %%%%%% step 4
    n = sqrt( sum( X.^2, 2 ) );
    n( n == 0 ) = 1; % patch to overcome rows with zero norm
    Y = bsxfun( @rdivide, X, n ); % divide by norm


    %%%%%% step 5
    clusters = kmeans(Y, k);

    %%%%%% step 6
    G = graph(A);
    figure;
    set(gcf,'position',[100,100,1000,800]);
    h = plot(G, "EdgeColor", "#bdc3c7", "MarkerSize", 6, "NodeFontSize", 10);
    title("path=" + path + " k=" + k);
    for c = 1:k
        highlight(h, find(clusters==c), 'NodeColor', string(colors(c))); 
    end
end